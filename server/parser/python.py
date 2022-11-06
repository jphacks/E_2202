import re
from typing import (
    Callable,
    Optional,
)

from container_class import (
    HighlightTextInfo,
    TextIndices,
    TextType
)


error_name_pattern = re.compile(r"(.+)?[e|E]rror.+")
not_found_pattern = re.compile(r".*N(ot|OT)[ |_]?F(ound|OUND).+")
url_pattern = re.compile(
    r"http(s)?:\/\/[\w./%-]+(\:\d{1,})?(\?)?(((\w+)=?[\w,%0-9]+)&?)*"
)
unix_path_pattern = re.compile(r"[\"\']?(\.)?(\/)?\w+\/[^\"\'\) ]+[\"\']?")


def find_pyfile(line: str) -> Optional[tuple[str, TextIndices]]:
    """Find python file path from input
    >>> find_pyfile('/usr/local/lib/python3.10/site-packages/uvicorn/importer.py')
    ('/usr/local/lib/python3.10/site-packages/uvicorn/importer.py', TextIndices(start=0, end=59))
    >>> find_pyfile('File "/usr/local/lib/python3.10/site-packages/uvicorn/config.py", line 479, in load')
    ('/usr/local/lib/python3.10/site-packages/uvicorn/config.py', TextIndices(start=6, end=63))
    >>> find_pyfile(\
        '~/opt/anaconda3/lib/python3.7/site-packages/torch/nn/functional.py in nll_loss(input, target, weight,'\
        ' size_average, ignore_index, reduce, reduction)')
    ('~/opt/anaconda3/lib/python3.7/site-packages/torch/nn/functional.py', TextIndices(start=0, end=66))
    >>> find_pyfile('File "PPO.py", line 275, in <module>')
    ('PPO.py', TextIndices(start=6, end=12))
    """
    pyfile_pattern = re.compile(r"(\~|\/)?(\/|[a-zA-Z0-9._-])+\.py")
    pyfile_path = pyfile_pattern.search(line)
    if pyfile_path:
        return pyfile_path[0], TextIndices(pyfile_path.start(), pyfile_path.end())
    return None


def get_python_libs(lines: list[str]) -> tuple[list[HighlightTextInfo], list[HighlightTextInfo], list[HighlightTextInfo]]:
    """スタックトレースにあるライブラリを抽出する
    >>> get_python_libs(['File "/usr/local/lib/python3.10/multiprocessing/process.py", line 315, in _bootstrap'])
    ([], [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=32, end=47),\
 text='multiprocessing', type=<TextType.LIBRARY_NAME: 2>)], [])
    >>> get_python_libs(['File "/usr/local/lib/python3.10/site-packages/uvicorn/_subprocess.py",'\
        ' line 76, in subprocess_started'])
    ([], [], [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=46, end=53), text='uvicorn',\
 type=<TextType.LIBRARY_NAME: 2>)])
    >>> get_python_libs([\
        'File "/usr/local/lib/python3.10/doctest.py", line 1346, in __run',\
        'File "<doctest __main__.parse_error[1]>", line 1, in <module>',\
        'asyncio.run(parse_error(ErrorContents(**error_text_query)))',\
    ])
    ([], [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=32, end=39), text='doctest',\
 type=<TextType.LIBRARY_NAME: 2>)], [])
    >>> get_python_libs([\
        'File "/usr/local/lib/python3.10/multiprocessing/process.py", line 108, in run',\
        'File "/usr/local/lib/python3.10/site-packages/uvicorn/_subprocess.py", line 76, in subprocess_started',\
        'File "/usr/local/lib/python3.10/asyncio/runners.py", line 44, in run'\
    ])
    ([], [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=32, end=47),\
 text='multiprocessing', type=<TextType.LIBRARY_NAME: 2>),\
 HighlightTextInfo(row_idx=3, col_idxes=TextIndices(start=32, end=39),\
 text='asyncio', type=<TextType.LIBRARY_NAME: 2>)],\
 [HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=46, end=53),\
 text='uvicorn', type=<TextType.LIBRARY_NAME: 2>)])
    >>> get_python_libs([\
        'File "/usr/local/lib/python3.8/dist-packages/uvicorn/_subprocess.py", line 76, in subprocess_started',\
        'File "/usr/local/lib/python3.8/dist-packages/torch/nn/modules/module.py", line 889, in _call_impl',\
    ])
    ([], [], [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=45, end=52),\
 text='uvicorn', type=<TextType.LIBRARY_NAME: 2>),\
 HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=45, end=50),\
 text='torch', type=<TextType.LIBRARY_NAME: 2>)])
    >>> get_python_libs([\
        'Traceback (most recent call last):',\
        '  File "PPO.py", line 275, in <module>',\
        '    stats = ppo_trainer.step(query_tensors, response_tensors, rewards)',\
        '  File "/opt/conda/lib/python3.8/site-packages/trl/ppo.py", line 134, in step',\
        '    assert bs == len(queries), f"Batch size ({bs}) does not match number of examples ({len(queries)})"',\
        'AssertionError: Batch size (64) does not match number of examples (18)"'\
    ])
    ([HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=8, end=14),\
 text='PPO.py', type=<TextType.YOUR_OWN_FILE_NAME: 3>),\
 HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=17, end=25),\
 text='line 275', type=<TextType.LINE_NUMBER: 4>),\
 HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=4, end=70),\
 text='stats = ppo_trainer.step(query_tensors, response_tensors, rewards)', type=<TextType.ERROR_MESSAGE: 0>)], [], \
 [HighlightTextInfo(row_idx=4, col_idxes=TextIndices(start=47, end=50),\
 text='trl', type=<TextType.LIBRARY_NAME: 2>)])
    """

    PYTHON3 = 'python3.'
    SITE_PACKAGES = 'site-packages'
    DIST_PACKAGES = 'dist-packages'

    def _extract_libname(path: str, indices: TextIndices, target: str) -> tuple[str, TextIndices]:
        """
        >>> _extract_libname(\
"/usr/local/lib/python3.8/dist-packages/torch/nn/modules/module.py", TextIndices(start=0, end=65), DIST_PACKAGES)
        ('torch', TextIndices(start=39, end=44))
        """
        pre, suc = path.split(target)
        t, libname, *_ = suc.split('/')  # t には /python3.10/ の .10 などが入る可能性がある
        libname = libname.replace('.py', '')
        start = 1 + indices.start + len(pre+target) + len(t)
        end = start + len(libname)
        return libname, TextIndices(start, end)

    def extract_libnames(target: str, filter_: Callable[[tuple[int, tuple[str, TextIndices]]], bool],
                         fnames: list[tuple[int, tuple[str, TextIndices]]]
                         ) -> list[tuple[int, tuple[str, TextIndices]]]:
        paths = filter(filter_, fnames)
        return [(row_idx, _extract_libname(path, indices, target)) for row_idx, (path, indices) in paths]

    def transform(input_: tuple[int, tuple[str, TextIndices]]) -> HighlightTextInfo:
        (row_idx, (text, indices)) = input_
        return HighlightTextInfo(row_idx, indices, text, TextType.LIBRARY_NAME)

    fname_in_stack = filter(lambda x: (x[0], x[1].startswith('File "')), enumerate(lines, start=1))
    _fnames = [(row_idx, find_pyfile(line))for row_idx, line in fname_in_stack]
    fnames = [(row_idx, pyfile) for row_idx, pyfile in _fnames if pyfile is not None]
    # 外部ライブラリを抽出
    site_packages = map(transform, extract_libnames(SITE_PACKAGES, lambda x: SITE_PACKAGES in x[1][0], fnames))
    dist_packages = map(transform, extract_libnames(DIST_PACKAGES, lambda x: DIST_PACKAGES in x[1][0], fnames))
    # 標準ライブラリを抽出
    stdlibs = map(transform, extract_libnames(
        PYTHON3, lambda x: (PYTHON3 in x[1][0]) and (SITE_PACKAGES not in x[1][0]) and (DIST_PACKAGES not in x[1][0]),
        fnames
    ))
    return [], sorted(stdlibs), sorted(list(site_packages) + list(dist_packages))


def error_parser(error: str) -> list[HighlightTextInfo]:
    """
    """
    lines = error.rstrip('\n').splitlines()
    row_idx, last_line = len(lines), lines[-1]
    # URL は検索クエリに使えないので除去するが，FILE情報の位置はそのまま保持しておく
    error_text = url_pattern.sub('', last_line)
    error_text = unix_path_pattern.sub('', error_text)

    user_scripts, stdlibs, extlibs = get_python_libs(lines)
    last_message = HighlightTextInfo(row_idx, TextIndices(0, len(last_line)), error_text, TextType.ERROR_MESSAGE)
    return [*stdlibs, *extlibs, last_message]
