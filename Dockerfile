FROM python:latest

WORKDIR /app

COPY requirements.txt /app/
COPY hello_docker.py /app/
RUN pip install -r requirements.txt

COPY . /app/

ENTRYPOINT ["python"]
CMD ["hello_docker.py"]