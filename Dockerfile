# FROM python:3.13.0a6-alpine3.18
FROM python

WORKDIR /app

COPY . .

RUN pip install -r requirments.txt

# ENTRYPOINT ["/app/wait-for-postgres.sh" ,"python", "app.py"]
ENTRYPOINT ["python", "app.py"]

CMD ["-s", "data/students.json", "-r", "data/rooms.json", "-f", "json"]