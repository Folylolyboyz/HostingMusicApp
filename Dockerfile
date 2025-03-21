# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip

# Copy requirements.txt first to improve caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose ports for both services
EXPOSE 3000
EXPOSE 8000

# Run main.py
CMD ["python", "together_run.py"]
