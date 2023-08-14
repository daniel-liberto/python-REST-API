FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# localhost
# CMD ["flask", "run", "--host", "0.0.0.0"]

# deploy
CMD ["gunicorn", "--bind", "--host", "0.0.0.0:80", "app:create_app()"]
