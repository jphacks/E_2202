import re

from typing import (
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
jsfile_pattern = re.compile(r'(\/.*?\.[js]+)')
jserror_line_pattern = re.compile(r'(:\d(:\d|\d)*)')


def find_jsfile(line: str) -> Optional[tuple[str, TextIndices]]:
    """Find javascript file path from input
    >>> find_jsfile('/home/soto/.tmp/testredsh/test.js')
    ('/home/soto/.tmp/testredsh/test.js', TextIndices(start=0, end=33))
    >>> find_jsfile('    at Object.<anonymous> (/home/soto/.tmp/testredsh/test.js:1:9)')
    ('/home/soto/.tmp/testredsh/test.js', TextIndices(start=27, end=60))
    """
    jsfile_path = jsfile_pattern.search(line)
    if jsfile_path:
        return jsfile_path[0], TextIndices(jsfile_path.start(), jsfile_path.end())
    return None


def error_parser(error: str) -> list[HighlightTextInfo]:
    """
    >>> error_parser('TypeError [ERR_INVALID_ARG_TYPE]: \
The "path" argument must be of type string. Received type number (3)')
    [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=0, end=102), \
text='TypeError [ERR_INVALID_ARG_TYPE]: \
The "path" argument must be of type string. Received type number (3)', type=<TextType.ERROR_MESSAGE: 1>)]
    >>> error_parser("Uncaught Error: Cannot find module 'path'")
    [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=0, end=41), \
text="Uncaught Error: Cannot find module 'path'", type=<TextType.ERROR_MESSAGE: 1>)]
    >>> error_parser(("hogehoge\\nUncaught Error: Cannot find module 'path'"))
    [HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=0, end=41), \
text="Uncaught Error: Cannot find module 'path'", type=<TextType.ERROR_MESSAGE: 1>)]
    >>> error_parser('/home/soto/.tmp/testredsh/test.js')
    [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=0, end=33), \
text='/home/soto/.tmp/testredsh/test.js', type=<TextType.LIBRARY_NAME: 2>)]
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

        error_file = find_jsfile(line)
        if error_file:
            error_path, error_idx = error_file
            error_list.append(HighlightTextInfo(idx + 1, error_idx, error_path, TextType.LIBRARY_NAME))
            # ここからエラー行番号を抽出する処理を書く
            ret = jserror_line_pattern.search(line[error_idx.end:])
            if ret:
                error_ind = TextIndices(ret.start() + 1 + error_idx.end, ret.end() + error_idx.end)
                error_list.append(HighlightTextInfo(idx + 1, error_ind, ret.groups()[0][1:], TextType.LIBRARY_NAME))
    return [*error_list]
