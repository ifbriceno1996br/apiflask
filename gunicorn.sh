#!/bin/bash
#gunicorn --chdir app app:app -w 2 --threads 2 -b 0.0.0.0:80
gunicorn --bind 0.0.0.0:80 app:app