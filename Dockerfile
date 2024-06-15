ROM python:3.10.12-slim-bullseye

WORKDIR /app

# Copy only the requirements file to leverage Dockercompose cache
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port that the app runs on
EXPOSE 8081


# Define the command to run the application
CMD ["python3", "bot.py"]

