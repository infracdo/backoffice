FROM python:3.13

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application explicitly
COPY . .

# Debug: List contents to verify copy worked
RUN echo "=== Contents of /app ===" && ls -la /app/

# Verify critical files exist
RUN test -f /app/app.py || (echo "ERROR: app.py not found!" && exit 1)
RUN test -f /app/entrypoint.py || (echo "ERROR: entrypoint.py not found!" && exit 1)

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 5050

# Use the custom entrypoint script
CMD ["python", "entrypoint.py"]
