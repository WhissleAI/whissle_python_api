# vortex_api
Multi-modal python API

## Installation
`pip install .`

## Running the App
`flask run --app audio_api.app:create_app`

## Running the API on a server

```
#!/bin/bash
export FLASK_APP=audio_api.app:create_app
export FLASK_ENV=development
flask run
```

