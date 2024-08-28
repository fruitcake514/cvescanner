# Use debian:bookworm-slim as the base image
FROM debian:bookworm-slim

# Install Git and Python
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip

# Clone the repository
RUN git clone https://github.com/fruitcake514/cvescanner.git /app/cvescanner

# Set the working directory
WORKDIR /app/cvescanner

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Specify the command to run the application
CMD ["python3", "app.py"]
