FROM python:3.11 AS prod
LABEL authors="yasha"

COPY ./backend/ /urlslab-bot/

WORKDIR /urlslab-bot

RUN python -m pip cache purge
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN useradd --create-home appuser
USER appuser

EXPOSE 9010

# Setting the number of workers to for fastapi
ENV WEB_CONCURRENCY=10

CMD [ "uvicorn", "core.server:app", "--host", "0.0.0.0", "--port", "9010" ]
