# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.12-slim-bullseye

RUN apt-get update 
RUN apt-get install apt-file -y
RUN apt-file update
RUN apt-get install -y python3-dev build-essential

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app

#CMD uvicorn main:app --host 0.0.0.0 --port $PORT