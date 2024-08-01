# Ai-Keiry

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

