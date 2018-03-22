#!/bin/bash
echo %1
set PYTHONPATH=%1
start "First" /wait py runner/n_times_runner.py -if .data/append-apps-clothing_jewelry-movies/docs -hf .data/append-apps-clothing_jewelry-movies/hashes -nc 9 -n 3 -o .data/append-apps-clothing_jewelry-movies/result_9.json  -om .data/append-apps-clothing_jewelry-movies/models9
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Second" /wait py runner/n_times_runner.py -if .data/append-beauty-gourmet-pets/docs -hf .data/append-beauty-gourmet-pets/hashes -nc 9 -n 3 -o .data/append-beauty-gourmet-pets/result_9.json -om .data/append-beauty-gourmet-pets/models9
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Third" /wait py runner/n_times_runner.py -if .data/append-books-cell_accessories-sports_outdoors/docs -hf .data/append-books-cell_accessories-sports_outdoors/hashes -nc 9 -n 3 -o .data/append-books-cell_accessories-sports_outdoors/result_9.json -om .data/append-books-cell_accessories-sports_outdoors/models9
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Fourth" /wait py runner/n_times_runner.py -if .data/replace-apps-clothing_jewelry-movies/docs -hf .data/replace-apps-clothing_jewelry-movies/hashes -nc 9 -n 3 -o .data/replace-apps-clothing_jewelry-movies/result_9.json  -om .data/replace-apps-clothing_jewelry-movies/models9
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Fifth" /wait py runner/n_times_runner.py -if .data/replace-beauty-gourmet-pets/docs -hf .data/replace-beauty-gourmet-pets/hashes -nc 9 -n 3 -o .data/replace-beauty-gourmet-pets/result_9.json  -om .data/replace-beauty-gourmet-pets/models9
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Sixth" /wait py runner/n_times_runner.py -if .data/replace-books-cell_accessories-sports_outdoors/docs -hf .data/replace-books-cell_accessories-sports_outdoors/hashes -nc 9 -n 3 -o .data/replace-books-cell_accessories-sports_outdoors/result_9.json -om .data/replace-books-cell_accessories-sports_outdoors/models9§

start "Seventh" /wait py runner/n_times_runner.py -if .data/append-apps-clothing_jewelry-movies/docs -hf .data/append-apps-clothing_jewelry-movies/hashes -nc 3 -n 3 -o .data/append-apps-clothing_jewelry-movies/result_3.json -om .data/append-apps-clothing_jewelry-movies/models3
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Eight" /wait py runner/n_times_runner.py -if .data/append-beauty-gourmet-pets/docs -hf .data/append-beauty-gourmet-pets/hashes -nc 3 -n 3 -o .data/append-beauty-gourmet-pets/result_3.json -om .data/append-beauty-gourmet-pets/models3
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Ninth" /wait py runner/n_times_runner.py -if .data/append-books-cell_accessories-sports_outdoors/docs -hf .data/append-books-cell_accessories-sports_outdoors/hashes -nc 3 -n 3 -o .data/append-books-cell_accessories-sports_outdoors/result_3.json -om .data/append-books-cell_accessories-sports_outdoors/models3
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Tenth" /wait py runner/n_times_runner.py -if .data/replace-apps-clothing_jewelry-movies/docs -hf .data/replace-apps-clothing_jewelry-movies/hashes -nc 3 -n 3 -o .data/replace-apps-clothing_jewelry-movies/result_3.json -om .data/replace-apps-clothing_jewelry-movies/models3
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Eleventh" /wait py runner/n_times_runner.py -if .data/replace-beauty-gourmet-pets/docs -hf .data/replace-beauty-gourmet-pets/hashes -nc 3 -n 3 -o .data/replace-beauty-gourmet-pets/result_3.json -om .data/replace-beauty-gourmet-pets/models3
ping 192.0.2.2 -n 1 -w 10000 > nul
start "Twelfth" /wait py runner/n_times_runner.py -if .data/replace-books-cell_accessories-sports_outdoors/docs -hf .data/replace-books-cell_accessories-sports_outdoors/hashes -nc 3 -n 3 -o .data/replace-books-cell_accessories-sports_outdoors/result_3.json -om .data/replace-books-cell_accessories-sports_outdoors/models3

Shutdown computer when done
shutdown.exe /s /t 00