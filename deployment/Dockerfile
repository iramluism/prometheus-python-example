
FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip
RUN pip install fastapi uvicorn prometheus_client

RUN mkdir /opt/my_project/ -p 

WORKDIR /opt/my_project

CMD ["uvicorn", "main:app", "--port", "8000"]
