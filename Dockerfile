# Base python-debian image
FROM python:3.9-slim-bullseye

# Copy the current directory contents into the container at /docker-togohub
ADD . /docker-togohub

# Set the working directory to /docker-togohub
WORKDIR /docker-togohub

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]