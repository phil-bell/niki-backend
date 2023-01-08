FROM python:3.11-alpine as build

WORKDIR /server/

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /server/

RUN pip install -r requirements.txt

COPY . /server/

RUN python manage.py migrate

FROM build as dev

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM build as prod

CMD ["uwsgi", "--socket", ":8000", "--module", "app.wsgi", "--threads", "4", "--chmod-socket=666"]


# Build command:
# docker build --target dev -t niki-backend .

# Start command: 
# docker run --rm -it --name niki-backend --volume $(pwd):/server -p 8000:8000 niki-backend

# Migrate command:
# docker exec --tty niki-backend python manage.py makemigrations
# docker exec --tty niki-backend python manage.py migrate