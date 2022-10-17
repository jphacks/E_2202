FROM python:3.10.4 as base

RUN pip install fastapi uvicorn
ENTRYPOINT  ["uvicorn", "--host", "0.0.0.0", "main:app"]

FROM base as dev

RUN pip install mypy 
RUN pip install requests
RUN pip install pytest
RUN pip install flake8
RUN pip install black
CMD  ["--reload"]
