FROM python:3.11-slim

WORKDIR /app

# Install system packages (including sqlite3)
RUN apt-get update && apt-get install -y sqlite3 && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

EXPOSE 83

CMD ["python", "app.py"]

