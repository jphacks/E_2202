FROM python:3.10.4 as base

RUN pip install fastapi uvicorn

FROM base as dev

RUN pip install mypy 

# CMD ["ここでfastAPIを走らせる（デバッグモードで実行したい）"]