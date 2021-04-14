FROM python:3.7

EXPOSE 8888

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements /usr/src/app/requirements
RUN pip install --no-cache-dir -r ./requirements/dev.txt

COPY ./irdb .

ENTRYPOINT ["python3", "irdb.py"]