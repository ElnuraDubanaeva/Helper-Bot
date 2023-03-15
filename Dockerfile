FROM python:3.10

EXPOSE 4464

RUN mkdir -p /opt/services/ggeek
WORKDIR /opt/services/ggeek

RUN mkdir -p /opt/services/geektech-back/requirements
ADD requirements.txt opt/services/ggeek/
COPY . /opt/services/ggeek/

RUN pip install -r requirements.txt
CMD ["python","bot/main.py"]






