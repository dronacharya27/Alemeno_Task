FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

EXPOSE 8000


CMD ["gunicorn", "credit_approval_system.wsgi:application", "--bind", "0.0.0.0:8000"]
