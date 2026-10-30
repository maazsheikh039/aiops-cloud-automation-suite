FROM python:3.9-slim

WORKDIR /app

RUN pip install flask requests

COPY retail_app.py .

ENV APP_VERSION=1.0.0

EXPOSE 5000

CMD ["python", "retail_app.py"]
