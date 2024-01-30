FROM python:3.11-slim-buster

WORKDIR /usr/src/app

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

EXPOSE 5000

# Use gunicorn for production
CMD ["python", "main.py"]


