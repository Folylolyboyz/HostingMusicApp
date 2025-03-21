    # Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for both services
EXPOSE 3000
EXPOSE 8000

# Run main.py
CMD ["python", "together_run.py"]
