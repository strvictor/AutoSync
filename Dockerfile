FROM python:3.12.7-alpine3.20

WORKDIR /core

COPY requeriments.txt /core/

RUN pip install --no-cache-dir -r requeriments.txt

COPY . /core/

EXPOSE 8000

#CMD sh -c "gunicorn core.wsgi:application --bind 0.0.0.0:$PORT"

CMD [ "sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000" ]