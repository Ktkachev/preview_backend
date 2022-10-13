from importlib.resources import path
import os
import argparse
from os import listdir
from os.path import isfile, join
import requests
from loaders.uploader import Uploader

base_url = "http://localhost:8000/api/preview/create/"
base_youtube_url = "https://www.youtube.com/watch?v="

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='input folder')
    parser.add_argument('--type', help='set name of model/random')
    args = parser.parse_args()
    return args


def send_request(link_to_video: str, s3_key, type: str):
    response = requests.post(base_url, json={'link_to_video': link_to_video, \
         's3_key': s3_key, 'type': type, 'votes': 0})
    return response

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

#path = "/home/kirill/Documents/final_project_dataset/test_output/"
#type = "maniqa"

def main():
    args = parse_args()
    path = args.input
    type = args.type
    
    uploader = Uploader()
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        print(path + file)
        key = uploader.upload(path + file) 
        print(key)
        response = send_request(link_to_video=(base_youtube_url + os.path.basename(find_between(file, '[', ']'))), \
            s3_key=key, type=type)
        print(response)

if __name__ == '__main__':
    main()
            


    

    

