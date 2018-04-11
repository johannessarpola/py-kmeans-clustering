#!/bin/bash
echo %1
set PYTHONPATH=%1
start "First" /wait py runner/n_times_runner.py -if .data/input/append-apps-clothing_jewelry-movies/docs -hf .data/input//append-apps-clothing_jewelry-movies/hashes -nc 9 -n 3 -o .data/dbscan-append-apps-clothing_jewelry-movies/result_9.json  -om .data/append-apps-clothing_jewelry-movies/models9
start "Second" /wait py runner/n_times_runner.py -if .data/input/append-beauty-gourmet-pets/docs -hf .data/input//append-beauty-gourmet-pets/hashes -nc 9 -n 3 -o .data/dbscan-append-beauty-gourmet-pets/result_9.json -om .data/append-beauty-gourmet-pets/models9
start "Third" /wait py runner/n_times_runner.py -if .data/input/append-books-cell_accessories-sports_outdoors/docs -hf .data/input//append-books-cell_accessories-sports_outdoors/hashes -nc 9 -n 3 -o .data/dbscan-append-books-cell_accessories-sports_outdoors/result_9.json -om .data/append-books-cell_accessories-sports_outdoors/models9
start "Fourth" /wait py runner/n_times_runner.py -if .data/input/replace-apps-clothing_jewelry-movies/docs -hf .data/input//replace-apps-clothing_jewelry-movies/hashes -nc 9 -n 3 -o .data/dbscan-replace-apps-clothing_jewelry-movies/result_9.json  -om .data/replace-apps-clothing_jewelry-movies/models9
start "Fifth" /wait py runner/n_times_runner.py -if .data/input/replace-beauty-gourmet-pets/docs -hf .data/input//replace-beauty-gourmet-pets/hashes -nc 9 -n 3 -o .data/dbscan-replace-beauty-gourmet-pets/result_9.json  -om .data/replace-beauty-gourmet-pets/models9
start "Sixth" /wait py runner/n_times_runner.py -if .data/input/replace-books-cell_accessories-sports_outdoors/docs -hf .data/input//replace-books-cell_accessories-sports_outdoors/hashes -nc 9 -n 3 -o .data/dbscan-replace-books-cell_accessories-sports_outdoors/result_9.json -om .data/replace-books-cell_accessories-sports_outdoors/models9

REM Shutdown computer when done
REM shutdown.exe /s /t 00