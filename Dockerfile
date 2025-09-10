FROM python:3.11-slim

WORKDIR /app

# Install required Python packages
RUN pip install --no-cache-dir requests

# Copy the test script
COPY test_embeddings.py /app/

# Make the script executable
RUN chmod +x test_embeddings.py

# Run the test script
CMD ["python", "test_embeddings.py"]
