# 1. Use the official Python 3.10 image as the base
FROM python:3.10

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy the entire project into the container
COPY . /app/

# 6. Expose the port the Django app runs on
EXPOSE 8000

# 7. Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
