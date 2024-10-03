# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port if necessary (optional for telegram bots)
EXPOSE 8443

# Set the environment variable for Python
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "./main.py"]
