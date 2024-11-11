FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev build-essential python3 python3-pip

RUN pip install virtualenv

RUN python -m venv venv

RUN source venv/bin/activate

COPY ./requirements.txt /app/requirements.txt

RUN venv/bin/pip install --no-cache-dir -r /app/requirements.txt 

COPY . /code/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]
