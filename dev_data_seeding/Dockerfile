FROM python:3.6.4-alpine3.7

RUN pip install pipenv

COPY Pipfile* /
RUN pipenv install --deploy --system

COPY mongo_data_seeding.py /
COPY *.json /
CMD python3 /mongo_data_seeding.py