#!/bin/sh

uvicorn fooball_base.main:app --host 0.0.0.0 --port 8000 --reload
