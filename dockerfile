# Use a minimal Linux base image
FROM alpine:latest

# Install system dependencies
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    cron

# Set the working directory
WORKDIR /app

# Copy the entire project
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Add cron job for running reddit-comp.py every 24 hours at 8am
RUN echo "0 8 * * * python3 /app/reddit/reddit-comp.py" >> /etc/crontabs/root

# Add cron job for running tweet.py every Monday at 8am
RUN echo "0 8 * * 1 python3 /app/twitter/tweet.py" >> /etc/crontabs/root

# Start cron daemon
CMD crond -l 2 -f
