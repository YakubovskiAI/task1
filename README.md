# task1
That project was created to solve task with some basic aspects like:
- loading data from json to database
- performing sql quries
- extracting data from database
- converting data
- docker compose
- using pre-commit

## How to install
Just clone this repository to your local machine. Then rename .env.example in .env and fill variables inside. And if u dont want to use docker - create(or choose remote) database server you want to use.

## How to use
### First way(without docker):

install all requirements:
```sh
$ pip install -r requirements.txt
```
And run app.py with three arguments
```sh
$ python3 app.py -s data/students.json -r data/rooms.json -f json
```
--students or -s -> argument with path to ur students.json file

--rooms or -r -> argument with path to ur rooms.json file

--format or -f -> optional argument with two possible formats "json" or "xml" (default is json)

### Second way(with docker):
Just run docker compose file with:
```sh
$ docker compose up
```
Or if you want all containers to stop after completing script:
```sh
$ docker-compose up --abort-on-container-exit
```

You can change arguments in Dockerfile. Default is:

CMD ["-s", "data/students.json", "-r", "data/rooms.json", "-f", "json"]
## Results
Results of performing scripts u will find in "data_results" directory. It will contain all queries results and folder with logs.