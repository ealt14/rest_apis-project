# CONTRIBUTING

## HOW TO RUN THE DOCKERFILE LOCALLY

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask_smorest_api sh -c "flask run --host 0.0.0.0"
```

```
from the command line, we can run: "docker build -t flask_smorest_api ."
then "docker run -p 5000:5000 flask_smorest_api"
```