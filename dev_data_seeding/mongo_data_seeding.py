#!/usr/bin/env python3.7

import os
import json
from pymongo import MongoClient


class MongoSeeder:

    def __init__(self):
        host = 'mongodb' if script_runs_within_container() else 'localhost'
        client = MongoClient(f'mongodb://root:rootpwd@{host}:27017')
        self.db = client.test

    def seed(self):
        print('Clearing artists collection...')
        self.db.artists.remove({})

        print('Inserting new artists...')
        artists = self.get_file_content('artists.json')
        self.db.artists.insert_many(artists)

        print('Clearing songs collection...')
        self.db.songs.remove({})

        print('Inserting new songs...')
        songs = self.get_file_content('songs.json')

        filtered_songs = []
        for song in songs:
            genre = song['Genre']
            year = song['Year']

            if year < 2016 and 'metal' in genre.lower():
                filtered_songs.append(song)

        self.db.songs.insert_many(filtered_songs)

        print('Done.')

    def get_file_content(self, file_name):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        if not os.path.exists(file_path):
            raise IOError('File: {} not available'.format(file_path))

        with open(file_name) as json_file:
            data = json.load(json_file)

        return data


def script_runs_within_container():
    with open('/proc/1/cgroup', 'r') as cgroup_file:
        return 'docker' in cgroup_file.read()


MongoSeeder().seed()
