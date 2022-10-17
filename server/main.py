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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

error_name_pattern = re.compile(".*[e|E]rror.+")
not_found_pattern = re.compile(".*N(ot|OT)[ |_]?F(ound|OUND).+")


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
            continue
        if not_found_pattern.match(line):
            result.append(line)
    return ImportantErrorLines(result=result)
