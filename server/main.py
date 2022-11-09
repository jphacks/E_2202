import re
from collections import Counter

from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware

from parser import (
    python,
    javascript,
    java,
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


def check_language(text: str) -> str:
    # 最頻値チェック
    ext_pattern = re.compile(r"(\.py|\.java|\.js|\.tsx)")
    candidates = ext_pattern.findall(text)
    if not candidates:
        return "Others"  # どれにも当てはまらなかったときは空で返す

    lang = Counter(candidates).most_common(1)[0][0]
    match lang:
        case ".py":
            res = "Python"
        case ".java":
            res = "Java"
        case ".js" | ".tsx":
            res = "JavaScript"
        case _:
            res = "Others"
    return res


@app.post("/error_parse", response_model=ImportantErrorLines)
async def parse_error(error_contents: ErrorContents) -> ImportantErrorLines:
    """
    Extract lines containing the word 'Error'
    >>> import asyncio
    >>> error_text_query = {\
        'error_text': "/path/to/file\\n AttributeError: 'int' object has no attribute 'append'", \
        'language': 'Python'}
    >>> asyncio.run(parse_error(ErrorContents(**error_text_query)))
    ImportantErrorLines(parser='Python', result=[\
HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=0, end=55), \
text=" AttributeError: 'int' object has no attribute 'append'", type=<TextType.ERROR_MESSAGE: 1>)])
    >>> error_text_query = {\
        'error_text': "Uncaught Error: Module parse failed: Duplicate export 'default' (26:7)", \
        'language': 'JavaScript'}
    >>> asyncio.run(parse_error(ErrorContents(**error_text_query)))
    ImportantErrorLines(parser='JavaScript', result=[\
HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=0, end=70), \
text="Uncaught Error: Module parse failed: Duplicate export 'default' (26:7)", type=<TextType.ERROR_MESSAGE: 1>)])
    """
    lang = error_contents.language
    if not lang:
        lang = check_language(error_contents.error_text)

    match lang:
        case 'Python':
            result = sorted(python.error_parser(error_contents.error_text))
        case 'Java':
            result = java.error_parser(error_contents.error_text)
        case 'JavaScript':
            result = sorted(javascript.error_parser(error_contents.error_text))
        case _:
            result = other.error_parser(error_contents.error_text)

    return ImportantErrorLines(parser=lang, result=result)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
