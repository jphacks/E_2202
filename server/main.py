from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware

from parser import (
    python,
    other,
)
from container_class import (
    ErrorContents,
    ImportantErrorLines,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yukusi.herokuapp.com",
        "http://yukusi.herokuapp.com",
        "https://yukusi-dev.herokuapp.com",
        "http://yukusi-dev.herokuapp.com",
        "https://youquery-jphacks.herokuapp.com",
        "http://youquery-jphacks.herokuapp.com",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/error_parse", response_model=ImportantErrorLines)
async def parse_error(error_contents: ErrorContents) -> ImportantErrorLines:
    """
    Extract lines containing the word 'Error'
    >>> import asyncio
    >>> error_text_query = {\
        'error_text': "/path/to/file\\n AttributeError: 'int' object has no attribute 'append'", \
        'language': 'Python'}
    >>> asyncio.run(parse_error(ErrorContents(**error_text_query)))
    ImportantErrorLines(result=[\
HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=0, end=55), \
text=" AttributeError: 'int' object has no attribute 'append'", type=<TextType.ERROR_MESSAGE: 1>)])
    """
    # TODO: 今後対応する言語が増えたらmatchに変更する方がいいかも
    if error_contents.language == 'Python':
        result = sorted(python.error_parser(error_contents.error_text))
        return ImportantErrorLines(result=result)

    result = other.error_parser(error_contents.error_text)
    return ImportantErrorLines(result=result)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
