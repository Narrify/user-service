FROM python:3.10-slim

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 9000

CMD ["uvicorn","app.main:app","--port","9000"]