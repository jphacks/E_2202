import re
from fastapi import (
    FastAPI,
)
from pydantic import (
    BaseModel,
)


app = FastAPI()
error_name_pattern = re.compile(".*[e|E]rror.+")
not_found_patter = re.compile(".*N(ot|OT)[ |_]?F(ound|OUND).+")


@app.get("/")
async def root():
    return {"message": "Hello World"}


class ErrorContents(BaseModel):
    error_text: str


@app.post("/error_parse")
async def parse_error(error_contents: ErrorContents):
    lines = error_contents.error_text.splitlines()
    result = []
    for line in lines:
        if error_name_pattern.match(line):
            result.append(line)
            continue
        if not_found_patter.match(line):
            result.append(line)
    return {"result": result}
