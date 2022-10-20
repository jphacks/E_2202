from dataclasses import dataclass
from enum import Enum, auto
import re
from typing import Callable
from fastapi import (
    FastAPI,
)
from pydantic import (
    BaseModel,
)
from fastapi.middleware.cors import CORSMiddleware


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


class TextType(Enum):
    ERROR_MESSAGE = auto()
    LIBRARY_NAME = auto()


@dataclass
class TextIndices:
    start: int
    end: int


@dataclass
class HighliteInfo:
    row_idx: int
    col_idxes: TextIndices
    text: str
    type: TextType


def find_pyfile(line: str) -> str:
    """Find python file path from input
    >>> find_pyfile('/usr/local/lib/python3.10/site-packages/uvicorn/importer.py')
    ('/usr/local/lib/python3.10/site-packages/uvicorn/importer.py', TextIndices(start=1, end=59))
    >>> find_pyfile('File "/usr/local/lib/python3.10/site-packages/uvicorn/config.py", line 479, in load')
    ('/usr/local/lib/python3.10/site-packages/uvicorn/config.py', TextIndices(start=7, end=63))
    >>> find_pyfile(\
        '~/opt/anaconda3/lib/python3.7/site-packages/torch/nn/functional.py in nll_loss(input, target, weight,'\
        ' size_average, ignore_index, reduce, reduction)')
    ('~/opt/anaconda3/lib/python3.7/site-packages/torch/nn/functional.py', TextIndices(start=1, end=66))
    >>> find_pyfile('File "PPO.py", line 275, in <module>')
    ('PPO.py', TextIndices(start=7, end=12))
    """
    pyfile_pattern = re.compile(r"(\~|\/)?(\/|[a-zA-Z0-9._-])+\.py")
    pyfile_path = pyfile_pattern.search(line)
    if pyfile_path:
        return pyfile_path[0]
    return ''


def get_python_libs(lines: list[str]) -> tuple[list[str], list[str]]:
    """スタックトレースにあるライブラリを抽出する
    >>> get_python_libs(['File "/usr/local/lib/python3.10/multiprocessing/process.py", line 315, in _bootstrap'])
    ([HighliteInfo(row_idx=1, col_idxes=TextIndices(start=33, end=47), text='multiprocessing', type=<TextType.LIBRARY_NAME: 2>)], [])
    >>> get_python_libs(['File "/usr/local/lib/python3.10/site-packages/uvicorn/_subprocess.py",'\
        ' line 76, in subprocess_started'])
    ([], [HighliteInfo(row_idx=1, col_idxes=TextIndices(start=47, end=53), text='uvicorn', type=<TextType.LIBRARY_NAME: 2>)])
    >>> get_python_libs([\
        'File "/usr/local/lib/python3.10/doctest.py", line 1346, in __run',\
        'File "<doctest __main__.parse_error[1]>", line 1, in <module>',\
        'asyncio.run(parse_error(ErrorContents(**error_text_query)))',\
    ])
    ([HighliteInfo(row_idx=2, col_idxes=TextIndices(start=33, end=39), text='doctest', type=<TextType.LIBRARY_NAME: 2>)], [])
    >>> get_python_libs([\
        'File "/usr/local/lib/python3.10/multiprocessing/process.py", line 108, in run',\
        'File "/usr/local/lib/python3.10/site-packages/uvicorn/_subprocess.py", line 76, in subprocess_started',\
        'File "/usr/local/lib/python3.10/asyncio/runners.py", line 44, in run'\
    ])
    ([HighliteInfo(row_idx=1, col_idxes=TextIndices(start=33, end=47), text='multiprocessing', type=<TextType.LIBRARY_NAME: 2>), HighliteInfo(row_idx=3, col_idxes=TextIndices(start=33, end=39), text='asyncio', type=<TextType.LIBRARY_NAME: 2>)], [HighliteInfo(row_idx=3, col_idxes=TextIndices(start=47, end=53), text='uvicorn', type=<TextType.LIBRARY_NAME: 2>)])
    >>> get_python_libs([\
        'File "/usr/local/lib/python3.8/dist-packages/uvicorn/_subprocess.py", line 76, in subprocess_started',\
        'File "/usr/local/lib/python3.8/dist-packages/torch/nn/modules/module.py", line 889, in _call_impl',\
    ])
    ([], [HighliteInfo(row_idx=1, col_idxes=TextIndices(start=46, end=50), text='torch', type=<TextType.LIBRARY_NAME: 2>), HighliteInfo(row_idx=1, col_idxes=TextIndices(start=46, end=52), text='uvicorn', type=<TextType.LIBRARY_NAME: 2>)])
    """

    PYTHON3 = 'python3.'
    SITE_PACKAGES = 'site-packages'
    DIST_PACKAGES = 'dist-packages'

    def _extract_libname(path: str, target: str) -> str:
        libname = path.split(target)[1].split('/')[1]
        return libname.replace('.py', '')

    def extract_libnames(target: str, filter_: Callable[[str], bool], fnames: list[str]) -> set[str]:
        paths = filter(filter_, fnames)
        return set(map(lambda x: _extract_libname(x, target), paths))

    fname_in_stack = filter(lambda line: line.startswith('File "'), lines)
    fnames = list(map(find_pyfile, fname_in_stack))
    # 外部ライブラリを抽出
    site_packages = extract_libnames(SITE_PACKAGES, lambda x: SITE_PACKAGES in x, fnames)
    dist_packages = extract_libnames(DIST_PACKAGES, lambda x: DIST_PACKAGES in x, fnames)
    # 標準ライブラリを抽出
    stdlibs = extract_libnames(
        PYTHON3, lambda x: (PYTHON3 in x) and (SITE_PACKAGES not in x) and (DIST_PACKAGES not in x),
        fnames
    )
    return sorted(stdlibs), sorted(site_packages | dist_packages)


def python_error(error: str) -> list[str]:
    """
    """
    lines = error.splitlines()
    result = []
    _, last_line = len(lines), lines[-1]
    error_type, *description = last_line.split(":")
    if error_type == "ImportError":
        error_text = unix_path_pattern.sub('__FILE__', last_line)
        result.append(
            error_text
            # HighliteInfo(row_idx=row_idx, col_idxes=(1, len(last_line)), text=error_text, type=TextType.ERROR_MESSAGE)
        )

    lines = [' '.join(line.split()) for line in error.splitlines()]
    stdlibs, extlibs = get_python_libs(lines)
    return [*stdlibs, *extlibs, last_line]


@app.post("/error_parse", response_model=ImportantErrorLines)
async def parse_error(error_contents: ErrorContents) -> ImportantErrorLines:
    """
    Extract lines containing the word 'Error'
    >>> import asyncio
    >>> error_text_query = {'error_text': "/path/to/file\\n AttributeError: 'int' object has no attribute 'append'"}
    >>> asyncio.run(parse_error(ErrorContents(**error_text_query)))
    ImportantErrorLines(result=[{
        "row_idx": 2,
        "col_idxes": {"start": 1, "end": 54},
        "text": " AttributeError: 'int' object has no attribute 'append'"
    }])
    """
    result = python_error(error_contents.error_text)
    return ImportantErrorLines(result=result)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
