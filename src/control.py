
import threading
import json
import os

from src.dash_master import ReadyVideoConfiguration




def edit_workspace(content):
    print(content)


def start_converted():
    queue_list = []

    config_list = [f for f in os.listdir('./options') if f.endswith('.json')]

    for index in config_list:
        with open(f'./options/{index}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            queue_list.append(data)

    
    video_coder = ReadyVideoConfiguration()
    for x in queue_list[0]:
        for y in queue_list[0][x]:
            video_coder.start(x, y)


# start_converted()

