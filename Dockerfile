FROM python:3.8

ARG DJANGO_SECRET_KEY


COPY . /file_manager

WORKDIR /file_manager

RUN pip install --no-cache-dir -r requirements.txt

ENV C_FORCE_ROOT="true"

EXPOSE 8000

CMD ["gunicorn", "file_manager.wsgi:application", "--bind", "0.0.0.0:8000"]
