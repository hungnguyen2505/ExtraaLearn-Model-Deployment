
# Use Python 3.12
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask application and trained model
COPY app.py .
COPY extraalearn_pipeline.joblib .

# Expose API port
EXPOSE 5000

# Start Flask API using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
