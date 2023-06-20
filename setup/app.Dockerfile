FROM python:3.11-alpine

WORKDIR /srv
COPY ./setup/requirements.txt ./
COPY ./src ./src
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.api:app"]