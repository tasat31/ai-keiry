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
$ streamlit run main.py
```

access to http://127.0.0.1:8501


# 2. Development

The following command is useful for development.

```
sqlite_web keiry.db
```

