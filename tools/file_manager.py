import json
import glob
from . import convert
import paramiko
import scp

from data_assets.point import Point

def save_path(key_points: list, sample_rate: float, folder_path: str, file_name: str):
    data = {}
    data["meta_data"] = {
        "path_name": file_name,
        "sample_rate": sample_rate
    }
    data["key_points"] = [p.to_json() for p in key_points]
    data["sampled_points"] = []
    #try:
    out_file = open(f"{folder_path}\\{file_name}.json", "w")
    json.dump(data, out_file, indent = 2)
    out_file.close()
    #except:
    #    print("Path was unable to be saved")

def load_path(file_path: str):
    try:
        with open(file_path) as json_save:
            data = json.load(json_save)
            key_points = []
            for p in data["key_points"]:
                key_points.append(Point(p["index"], p["delta_time"], p["x"], p["y"], p["angle"]))
                print("Path loaded successfully")
            return key_points, data["meta_data"]["sample_rate"]
    except:
        print("Path was unable to be loaded")
        return [], 0.01