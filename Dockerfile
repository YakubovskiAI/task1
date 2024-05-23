FROM python

WORKDIR /app

COPY . .

RUN pip install -r requirments.txt

ENTRYPOINT ["python", "app.py"]

CMD ["-s", "data/students.json", "-r", "data/rooms.json", "-f", "json"]