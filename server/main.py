import re
from fastapi import (
    FastAPI,
)
from pydantic import (
    BaseModel,
)
from fastapi.middleware.cors import CORSMiddleware
import asyncio



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yukusi.herokuapp.com",
        "https://yukusi-dev.herokuapp.com",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

error_name_pattern = re.compile(r"(.+)?[e|E]rror.+")
not_found_pattern = re.compile(r".*N(ot|OT)[ |_]?F(ound|OUND).+")
url_pattern = re.compile(
    r"http(s)?:\/\/[\w./%-]+(\:\d{1,})?(\?)?(((\w+)=?[\w,%0-9]+)&?)*"
)
unix_path_pattern = re.compile(r"[\"\']?(\/)?\w+\/[^\"\'\) ]+[\"\']?")


class ErrorContents(BaseModel):
    error_text: str


class ImportantErrorLines(BaseModel):
    result: list[str]


def find_pyfile(line: str) -> str:
    """Find python file path from input
    >>> find_pyfile('/usr/local/lib/python3.10/site-packages/uvicorn/importer.py')
    '/usr/local/lib/python3.10/site-packages/uvicorn/importer.py'
    >>> find_pyfile('File "/usr/local/lib/python3.10/site-packages/uvicorn/config.py", line 479, in load')
    '/usr/local/lib/python3.10/site-packages/uvicorn/config.py'
    >>> find_pyfile('~/opt/anaconda3/lib/python3.7/site-packages/torch/nn/functional.py in nll_loss(input, target, weight, size_average, ignore_index, reduce, reduction)')
    '~/opt/anaconda3/lib/python3.7/site-packages/torch/nn/functional.py'
    >>> find_pyfile('File "PPO.py", line 275, in <module>')
    'PPO.py'
    """
    pyfile_pattern = re.compile(r"(\~|\/)?(\/|[a-zA-Z0-9._-])+\.py")
    pyfile_path = pyfile_pattern.search(line)
    if pyfile_path:
        return pyfile_path[0]
    return ''


def python_error(error: str) -> str:
    """
    """
    last_line = error.splitlines()[-1]
    last_line = ' '.join(last_line.split())# 無駄なスペースの除去
    error_type, description = last_line.split(":")
    if error_type == "ImportError":
        return unix_path_pattern.sub('__FILE__', last_line)

    lines = [' '.join(line.split()) for line in error.splitlines()]
    fname_in_stack = filter(lambda line: line.startswith('FILE "'), lines)
    fnames = set(map(lambda x: find_pyfile, fname_in_stack))
    return last_line


@app.post("/error_parse", response_model=ImportantErrorLines)
async def parse_error(error_contents: ErrorContents) -> ImportantErrorLines:
    """
    Extract lines containing the word 'Error'
    >>> error_text_query = {'error_text': "/path/to/file\\n AttributeError: 'int' object has no attribute 'append'"}
    >>> asyncio.run(parse_error(ErrorContents(**error_text_query)))
    ImportantErrorLines(result=["AttributeError: 'int' object has no attribute 'append'"])
    """
    result = [python_error(error_contents.error_text)]
    return ImportantErrorLines(result=result)


if __name__ == "__main__":
    import doctest
    doctest.testmod()