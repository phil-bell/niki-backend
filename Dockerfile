FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG ENVIROMENT=dev
WORKDIR /code/
ADD requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
