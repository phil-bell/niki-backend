FROM python:3.11-alpine as build

WORKDIR /server/

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /server/

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del .pynacl_deps

COPY . /server/

RUN python manage.py migrate && python manage.py collectstatic --noinput

CMD ["uvicorn", "niki.asgi:application", "--host", "0.0.0.0", "--port", "8080"]


# CMD ["uvicorn", "-b", "0.0.0.0", "-p", "8000", "niki.asgi:application"]
# CMD ["uwsgi", "--socket", ":8000", "--module", "app.wsgi", "--threads", "4", "--chmod-socket=666"]
# Build command:
# docker build --target dev -t niki-backend .

# Start command:
# docker create --name niki-backend --volume $(pwd):/server -p 8000:8000 niki-backend
# docker start -ia niki-backend

# Migrate command:
# docker exec --tty niki-backend python manage.py makemigrations
# docker exec --tty niki-backend python manage.py migrate