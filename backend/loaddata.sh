#!/bin/sh

cd data/
python3 fixture_preparation.py
cd ..
python3 manage.py loaddata data/fixtures.json
