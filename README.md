# Craps

Emulate a game of craps

# Testing

Unit tests run with pytest inside a docker container

1 - Build container image (only need to do if requirements.txt has changed)
```shell
docker build -t craps .
```

2 - Run tests
```shell
docker run -tv {checkout_directory}:/craps craps pytest
```
where `checkout_directory` is the directory the repository has been cloned to, e.g. /home/username/code/craps

# Formatting

All test and source code is formatted with [black](https://github.com/psf/black). The container can run black with
```shell
docker run -tv {checkout_directory}:/craps craps black .
```

