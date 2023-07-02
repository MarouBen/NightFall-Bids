FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /nightFallBidsDocker

ADD . /nightFallBidsDocker/

COPY requirements.txt /nightFallBidsDocker/

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

COPY . /nightFallBidsDocker/

EXPOSE 8000

CMD ["python3", "manage.py", "runserver","0.0.0.0:8000"]