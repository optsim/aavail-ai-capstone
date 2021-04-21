FROM python:3.6-slim
COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install -y build-essential  && \
    apt-get install -y curl
RUN pip install -r requirements.txt
EXPOSE 80
WORKDIR /app
CMD ["python", "app.py"]