import re

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


def error_parser(error: str) -> list[HighlightTextInfo]:
    lines = error.rstrip('\n').splitlines()
    result = []
    for row_idx, line in enumerate(lines, start=1):
        if error_name_pattern.search(line) is None \
                and not_found_pattern.search(line) is None:
            continue

        # URLやファイル名を除去する
        res = url_pattern.sub("", line)
        res = unix_path_pattern.sub("", res)
        result.append(HighlightTextInfo(row_idx, TextIndices(0, len(line)), res, TextType.ERROR_MESSAGE))
    return result
