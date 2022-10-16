import re
from fastapi import (
    FastAPI,
)
from pydantic import (
    BaseModel,
)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class ErrorContents(BaseModel):
    error_text: str


@app.post("/error_parse")
async def parse_error(error_contents: ErrorContents):
    return {"result": error_contents.error_text}
