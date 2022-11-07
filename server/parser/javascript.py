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


url_pattern = re.compile(
    r"http(s)?:\/\/[\w./%-]+(\:\d{1,})?(\?)?(((\w+)=?[\w,%0-9]+)&?)*"
)
unix_path_pattern = re.compile(r"[\"\']?(\.)?(\/)?\w+\/[^\"\'\) ]+[\"\']?")
js_error_pattern = r'.*Error(\s\[.*\])?:.*'


def find_jsfile(line: str) -> Optional[tuple[str, TextIndices]]:
    """Find python file path from input
    >>> find_jsfile('/home/soto/.tmp/testredsh/test.ts')
    ('/home/soto/.tmp/testredsh/test.ts', TextIndices(start=0, end=33))
    >>> find_jsfile('    at Object.<anonymous> (/home/soto/.tmp/testredsh/test.ts:1:9)')
    ('/home/soto/.tmp/testredsh/test.ts', TextIndices(start=27, end=60))
    >>> find_jsfile("test.ts:5:23 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.")
    ('test.ts', TextIndices(start=0, end=7))
    >>> find_jsfile("ERROR in ./src/App.tsx 26:7")
    ('./src/App.tsx', TextIndices(start=9, end=22))
    """
    tsfile_pattern = re.compile(r'(\/.*?\.[js]+)')
    tsfile_path = tsfile_pattern.search(line)
    if tsfile_path:
        return tsfile_path[0], TextIndices(tsfile_path.start(), tsfile_path.end())
    return None

def js_error(error: str) -> list[HighlightTextInfo]:
    """ hoge
    >>> js_error('TypeError [ERR_INVALID_ARG_TYPE]: The "path" argument must be of type string. Received type number (3)')
    [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=0, end=102), \
text='TypeError [ERR_INVALID_ARG_TYPE]: The "path" argument must be of type string. Received type number (3)', type=<TextType.ERROR_MESSAGE: 1>)]
    >>> js_error("Uncaught Error: Cannot find module 'path'")
    [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=0, end=41), \
text="Uncaught Error: Cannot find module 'path'", type=<TextType.ERROR_MESSAGE: 1>)]
    >>> js_error(("hogehoge\\nUncaught Error: Cannot find module 'path'"))
    [HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=0, end=41), \
text="Uncaught Error: Cannot find module 'path'", type=<TextType.ERROR_MESSAGE: 1>)]
    >>> js_error('/home/soto/.tmp/testredsh/test.ts')
    [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=0, end=33), \
text='/home/soto/.tmp/testredsh/test.ts', type=<TextType.LIBRARY_NAME: 2>)]
    """
    lines = error.rstrip('\n').splitlines()
    # 一行ずつ見ていく
    error_list = []
    for idx, line in enumerate(lines):
        if re.search(js_error_pattern, line):
            # URL は検索クエリに使えないので除去するが，FILE情報の位置はそのまま保持しておく
            error_text = url_pattern.sub('', line)
            error_text = unix_path_pattern.sub('', error_text)
            first_message = HighlightTextInfo(idx + 1, TextIndices(0, len(line)), error_text, TextType.ERROR_MESSAGE)
            error_list.append(first_message)
        error_file  = find_jsfile(line)
        if error_file:
            error_list.append(HighlightTextInfo(idx + 1, error_file[1], error_file[0], TextType.LIBRARY_NAME))
    return [*error_list]
