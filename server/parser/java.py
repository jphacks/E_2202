import re

from container_class import (
    HighlightTextInfo,
    TextIndices,
    TextType
)


exception_name_pattern = re.compile(r"java.lang.+?.Exception")
url_pattern = re.compile(
    r"http(s)?:\/\/[\w./%-]+(\:\d{1,})?(\?)?(((\w+)=?[\w,%0-9]+)&?)*"
)
unix_path_pattern = re.compile(r"[\"\']?(\.)?(\/)?\w+\/[^\"\'\) ]+[\"\']?")
error_occurs_pattern = re.compile(r"\(\w+.java:\d\)")


def get_user_scripts(lines: list[str]) -> list[HighlightTextInfo]:
    """コード内にあるエラーの原因箇所を抽出する
    >>> get_user_scripts(['at sample.setArray(sample.java:7)'])
    [HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=19, end=30), \
text='sample.java', type=<TextType.USERS_FILE_NAME: 3>)]
    """
    user_scripts = []
    for row_idx, line in enumerate(lines, start=1):
        error_row = error_occurs_pattern.search(line)
        if error_row:
            res = url_pattern.sub("__URL__", error_row.group())
            res = unix_path_pattern.sub("__FILE__", res)
            # ファイル名とエラー行(EX sample.java:7)を分離させ、数字の部分を抽出する
            len_line_number = error_row.group().split(':')[1]

            start = error_row.start() + 1
            end = error_row.end() - len(len_line_number) - 1
            user_scripts.append(HighlightTextInfo(row_idx, TextIndices(start, end),
                                res[1:len(res) - len(len_line_number) - 1], TextType.USERS_FILE_NAME))

    return user_scripts


def error_parser(error: str) -> list[HighlightTextInfo]:
    """
    >>> error_parser('Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: \
        Index 20 out of bounds for length 10\\n \
        at sample.setArray(sample.java:7)\\n \
        at sample.main(sample.java:3)')
    [HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=28, end=39), \
text='sample.java', type=<TextType.USERS_FILE_NAME: 3>), \
HighlightTextInfo(row_idx=2, col_idxes=TextIndices(start=40, \
end=41), text='7', type=<TextType.LINE_NUMBER: 4>), HighlightTextInfo(row_idx=3, \
col_idxes=TextIndices(start=24, end=35), text='sample.java', \
type=<TextType.USERS_FILE_NAME: 3>), HighlightTextInfo(row_idx=3, \
col_idxes=TextIndices(start=36, end=37), text='3', type=<TextType.LINE_NUMBER: 4>), \
HighlightTextInfo(row_idx=1, col_idxes=TextIndices(start=27, end=67), \
text='java.lang.ArrayIndexOutOfBoundsException', type=<TextType.ERROR_MESSAGE: 1>)]
    """
    lines = error.rstrip('\n').splitlines()
    row_idx, first_line = 1, lines[0]

    # 'Exception'という文字を抽出する
    java_exception_obj = exception_name_pattern.search(first_line)
    error_message_row = []

    if java_exception_obj:
        error_text = url_pattern.sub('', java_exception_obj.group())
        error_text = unix_path_pattern.sub('', error_text)
        error_message_row.append(HighlightTextInfo(row_idx, TextIndices(java_exception_obj.start(),
                                 java_exception_obj.end()), error_text, TextType.ERROR_MESSAGE))

    user_scripts = get_user_scripts(lines)

    user_scripts_error_lines = []
    for user_script in user_scripts:
        user_scripts_error_lines.append(user_script)
        # エラーが出た行番号を取得
        message_line = lines[user_script.row_idx - 1]
        start = message_line.find(":")
        end = start + message_line[start:].find(")")
        user_scripts_error_lines.append(
            HighlightTextInfo(
                user_script.row_idx,
                TextIndices(start + 1, end),
                message_line[start + 1:end],
                TextType.LINE_NUMBER,
            )
        )

    return [*user_scripts_error_lines, *error_message_row]
