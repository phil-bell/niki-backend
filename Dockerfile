FROM python:3.11-alpine

WORKDIR /server/

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /server/

RUN pip install -r requirements.txt

COPY . /server/

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]