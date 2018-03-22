#!/bin/bash
echo %1
set PYTHONPATH=%1
start "First" /wait py runner/n_times_runner.py -if .data/append-apps-clothing_jewelry-movies/docs -hf .data/append-apps-clothing_jewelry-movies/hashes -nc 9 -n 3 -o .data/append-apps-clothing_jewelry-movies/result_9.json
start "Second" /wait py runner/n_times_runner.py -if .data/append-beauty-gourmet-pets/docs -hf .data/append-beauty-gourmet-pets/hashes -nc 9 -n 3 -o .data/append-beauty-gourmet-pets/result_9.json
start "Third" /wait py runner/n_times_runner.py -if .data/append-books-cell_accessories-sports_outdoors/docs -hf .data/append-books-cell_accessories-sports_outdoors/hashes -nc 9 -n 3 -o .data/append-books-cell_accessories-sports_outdoors/result_9.json
start "Fourth" /wait py runner/n_times_runner.py -if .data/replace-apps-clothing_jewelry-movies/docs -hf .data/replace-apps-clothing_jewelry-movies/hashes -nc 9 -n 3 -o .data/replace-apps-clothing_jewelry-movies/result_9.json
start "Fifth" /wait py runner/n_times_runner.py -if .data/replace-beauty-gourmet-pets/docs -hf .data/replace-beauty-gourmet-pets/hashes -nc 9 -n 3 -o .data/replace-beauty-gourmet-pets/result_9.json
start "Sixth" /wait py runner/n_times_runner.py -if .data/replace-books-cell_accessories-sports_outdoors/docs -hf .data/replace-books-cell_accessories-sports_outdoors/hashes -nc 9 -n 3 -o .data/replace-books-cell_accessories-sports_outdoors/result_9.json
