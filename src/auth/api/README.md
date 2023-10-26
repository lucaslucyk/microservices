# Auth API

## Create migration
```bash
$ alembic revision --autogenerate -m "<comment>"
```

## Migrate database
```bash
$ alembic upgrade head
```


## Run server

```bash
$ uvicorn main:app --reload
```

