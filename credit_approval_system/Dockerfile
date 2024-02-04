# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app


COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container

# Expose port 8000 for Django
EXPOSE 8000

# Command to run on container start
CMD ["gunicorn", "credit_approval_system.wsgi:application", "--bind", "0.0.0.0:8000"]
