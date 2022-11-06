import re

from container_class import (
    HighlightTextInfo,
    TextIndices,
    TextType
)


exception_name_pattern = re.compile(r"java.lang.+?:")
url_pattern = re.compile(
    r"http(s)?:\/\/[\w./%-]+(\:\d{1,})?(\?)?(((\w+)=?[\w,%0-9]+)&?)*"
)
unix_path_pattern = re.compile(r"[\"\']?(\.)?(\/)?\w+\/[^\"\'\) ]+[\"\']?")
error_occurs_pattern = re.compile(r"\(\w+.java:\d\)")

def get_error_occurs_row_in_code(lines: list[str]) -> list[HighlightTextInfo]:
    """コード内にあるエラーの原因箇所を抽出する
    >>> get_error_occurs_row_in_code(['at sample.setArray(sample.java:7)'])
    [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=18, end=33), \
text='(sample.java:7)', type=<TextType.ERROR_OCCURS_ROW_IN_CODE: 3>)]
    """
    error_occurs_rows = []
    for row_idx, line in enumerate(lines, start=1):
        error_row = error_occurs_pattern.search(line)
        if error_row:
            res = url_pattern.sub("__URL__", error_row.group())
            res = unix_path_pattern.sub("__FILE__", res)
            error_occurs_rows.append(HighlightTextInfo(row_idx, TextIndices(error_row.start(), \
                error_row.end()), res, TextType.ERROR_OCCURS_ROW_IN_CODE))

    return error_occurs_rows

def error_parser(error: str) -> list[HighlightTextInfo]:
    """
    >>> error_parser('Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 20 out of bounds for length 10\\n \
        at sample.setArray(sample.java:7)\\n \
        at sample.main(sample.java:3)')
    [HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=27, end=42), text='(sample.java:7)', \
type=<TextType.ERROR_OCCURS_ROW_IN_CODE: 3>), HighlightTextInfo(row_idx=3, \
col_idxes=TextIndices(start=23, end=38), text='(sample.java:3)', \
type=<TextType.ERROR_OCCURS_ROW_IN_CODE: 3>), HighlightTextInfo(row_idx=1, \
col_idxes=TextIndices(start=27, end=68), text='java.lang.ArrayIndexOutOfBoundsException:', type=<TextType.ERROR_MESSAGE: 1>)]
    """
    lines = error.rstrip('\n').splitlines()
    row_idx, first_line = 1, lines[0]

    # 'Exception'という文字を抽出する
    java_exception_obj = exception_name_pattern.search(first_line)
    error_message_row = []

    if java_exception_obj:
        error_text = url_pattern.sub('', java_exception_obj.group())
        error_text = unix_path_pattern.sub('', error_text)
        
        error_message_row.append(HighlightTextInfo(row_idx, TextIndices(java_exception_obj.start(), java_exception_obj.end()), error_text, TextType.ERROR_MESSAGE))

    error_occurs_rows_in_code = get_error_occurs_row_in_code(lines)
    
    return [*error_occurs_rows_in_code, *error_message_row]
