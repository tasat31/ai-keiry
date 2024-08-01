# Shipping Database

source: https://www.equasis.org/

# 1. Deployment

## 1-(1). Configure .env

```
$ cp env.example .env
```

## 1-(2). Lauching Docker container and login

```
$ docker compose build
$ docker compose up -d
$ docker exec -it ai-keiry bash
```

Linux
```
$ xhost +
```

## 1-(3). Database setup

```
$ alembic upgrade head
```

If some revisions exist, run the command followed
(add models to env.py)

```
$ alembic revision --autogenerate -m "Some comment"
```

## 1-(4). Execute streamlit

```
$ streamlit run app/dashboard.py
```

access to http://127.0.0.1:8502


# 2. Development

The following command is useful for development.

## 2-(1). playwright codegen for writing scraping scripts

```
$ playwright codegen https://www.equasis.org/
```

## 2-(2). Execute Robot

```
$ python3 robot.py scrape [imo_no]
```

```
$ python3 robot.py scrape_batch_process
```

## 2-(3). Execute luigi task from command line

```
$ luigi --module app.tasks.scrape_equasis ScrapeEquasisTask --imo-no=8300614 --local-scheduler
```

## 2-(4). Execute sqlite_web

```
sqlite_web shipping.db
```

# 3. Make exe files

You make exec files in the target host machine.(Windows, Linux supported)

## 3-(1) requirement

You need to set up virtualenv in the target host machine.

```
python3 and virtualenv
```


## 3-(2) Edit app.spec

* Choose your target environment

```
$ cp app.spec.linux app.spec
$ cp app.spec.windows10 app.spec
$ cp app.spec.windows11 app.spec
```

## 3-(2) Edit app.py

```
$ cp app.py.example app.py
```

modify `app.py`

```
"./dashboard.py" -> "/home/your/path/shipping-db/dashboard.py"
```

## 3-(3) Run Command

$ pyinstaller app.spec --clean


# 4. Run schedule batch proccess from python interpreter

## 4-(1) example

```
$ python3
Python 3.12.0 (main, Nov 29 2023, 03:23:09) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from schedules.scrape_equasis_job import ScrapeEquasisJob
>>> job = ScrapeEquasisJob(name='scrape_equasis_job')
>>> job.execute_job('19:00')

```

### Vessel Finderの実行手順

```
$ python3 robot.py vessel_finder_batch_process &
$ streamlit run dashboard_vessel_finder.py
```
