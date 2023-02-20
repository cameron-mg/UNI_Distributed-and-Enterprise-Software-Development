FROM python:3.11.0-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /daesd_group

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]