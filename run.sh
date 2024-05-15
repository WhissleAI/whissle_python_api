#!/bin/bash

export FLASK_APP=audio_api.app:create_app
export FLASK_ENV=development
flask run
