# Download images using flickr api

App downloads the highest resolution flickr images which allowed permission by owner

## Features

- Download link one by one
- Download multiple links set in file
- Write url from clipboard to file

## Installation

App requires **[python 3.x](https://www.python.org)** to run.

1. In **src/flickr** create 2 json files

    - flickr_api.json

    ```json
    {
        "api_key": "Your Api Key",
        "api_secret": "Your Api Secret",
        "api_url": "https://api.flickr.com/services/rest/"
    }
    ```
    - flickr_app.json

    ```json
    {
        "path_saved":"Your Path Saver"
    }
    ```

2. Install environment and packages and start app.

    ```sh
    pip install -r requirements.txt
    cd src
    python main.py
    ```