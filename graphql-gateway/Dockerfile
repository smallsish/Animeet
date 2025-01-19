# Use a base Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy project files to working directory
COPY . .

# Install a version of pip that is compatible with ariadne v 0.15.0
RUN pip install --upgrade pip==24.0
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=src.main.py
ENV FLASK_ENV=development

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
