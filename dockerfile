# Use a minimal Linux base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the entire project directory
COPY . .

# Create and activate a virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN . /app/venv/bin/activate

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set up cron jobs
RUN apt-get update && apt-get install -y cron
RUN echo "0 8 * * * python3 /app/reddit/reddit-comp.py" >> /etc/crontab
RUN echo "0 8 * * 1 python3 /app/twitter/tweet.py" >> /etc/crontab

# Run discord_main.py
CMD python reddit/reddit-comp.py && python discord_bot/discord_main.py && cron -f
