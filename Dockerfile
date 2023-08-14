FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# localhost
# CMD ["flask", "run", "--host", "0.0.0.0"]

# deploy
CMD ["/bin/bash", "docker-entrypoint.sh"]
