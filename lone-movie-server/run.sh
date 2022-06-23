#!/bin/bash
gunicorn --worker-class eventlet -b 0.0.0.0:5000 -w 1 lonemovie:lonemovie