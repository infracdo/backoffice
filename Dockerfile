FROM python:3.13-slim

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 5050

# Run diagnostic first, then try to start the app
CMD ["sh", "-c", "echo 'Running diagnostics...' && python diagnose.py && echo 'Starting app...' && python app.py"]
