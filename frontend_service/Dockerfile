FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask requests

EXPOSE 5000

CMD ["python", "frontend_service.py"]
