FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev build-essential python3 python3-pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt 

COPY . /code/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]
