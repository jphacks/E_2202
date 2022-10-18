import re
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
    allow_origins=["https://yukusi.herokuapp.com", "https://yukusi-dev.herokuapp.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

error_name_pattern = re.compile(r"(.+)?Error.+")
not_found_pattern = re.compile(r".*N(ot|OT)[ |_]?F(ound|OUND).+")
url_pattern = re.compile(
    r"http(s)?:\/\/[\w./%-]+(\:\d{1,})?(\?)?(((\w+)=?[\w,%0-9]+)&?)*"
)
unix_path_pattern = re.compile(r"[\"\']?(\/)?\w+\/[^\"\' ]+[\"\']?")


class ErrorContents(BaseModel):
    error_text: str


class ImportantErrorLines(BaseModel):
    result: list[str]


@app.post("/error_parse", response_model=ImportantErrorLines)
async def parse_error(error_contents: ErrorContents) -> ImportantErrorLines:
    lines = error_contents.error_text.splitlines()
    result = []
    for line in lines:
        if error_name_pattern.match(line):
            result.append(line)
        elif not_found_pattern.match(line):
            result.append(line)
    result = url_pattern.sub("__URL__", "\n".join(result)).split("\n")
    result = unix_path_pattern.sub("__FILE__", "\n".join(result)).split("\n")
    return ImportantErrorLines(result=result)
