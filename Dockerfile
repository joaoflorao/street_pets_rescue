FROM python:3.8-slim-buster
LABEL description="Street Pets Rescue"
WORKDIR /usr/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "main.py"]
