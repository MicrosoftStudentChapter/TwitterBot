# Use a minimal Linux base image
FROM alpine:latest

# Install system dependencies
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    cron

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache bash

# Copy the entire project directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set up cron jobs
RUN apk add --no-cache dcron

# Add the cron jobs
# Add cron job for running reddit-comp.py every 24 hours at 8am
RUN echo "0 8 * * * python3 /app/reddit/reddit-comp.py" >> /etc/crontabs/root

# Add cron job for running tweet.py every Monday at 8am
RUN echo "0 8 * * 1 python3 /app/twitter/tweet.py" >> /etc/crontabs/root

# Run discord_main.py
CMD python reddit/reddit-comp.py && python discord_bot/discord_main.py && crond -f
