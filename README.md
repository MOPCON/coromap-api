# Open Street Map API

## About The Project

// TBD 123

### Build With

* Python 3.8
* FastAPI

## Getting Started

### Prerequisites

* Firebase
* [Recommended] Docker and Docker Compose

### How to run

1. Get a service account credential json file from firebase.
2. Put the credential json file in `storage/serviceAccount.json`
3. Run docker-compose
    ```shell
    docker-compose up -d --build
    ```
4. Access the health check api see if everything works fine.
    ```shell
    curl localhost:38888/health
    ```

## Usage

### Import data from csv

The first initial data should be import by using csv file, But also can be added throw api for 
more detail please read the api document.
```shell
python import.py
```
