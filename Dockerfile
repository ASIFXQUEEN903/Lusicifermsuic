FROM python:3.10-slim-bullseye

# Install ffmpeg and Node.js
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg curl gnupg \
 && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
 && apt-get install -y nodejs \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
COPY . /app/
WORKDIR /app/

# Install Python requirements
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Start the app
CMD ["bash", "start"]
