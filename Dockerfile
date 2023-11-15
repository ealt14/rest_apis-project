FROM python:3.11
#tell the docker desktop what port to run the app in
EXPOSE 5000
#specify the app directory to use in the image
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
#specify where you want to copy the current directory from and into
COPY . .
#allows an external client to make a request to the container
CMD ["flask", "run", "--host", "0.0.0.0"]