FROM python:3.11

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]

# $ docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api