#!/bin/sh

uvicorn fooball_base.main:app --host 0.0.0.0 --port 7000 --reload
