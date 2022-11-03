import json
import glob
from . import convert
import paramiko
import scp

from data_assets.point import Point
from SplineGeneration import generateSplines

def get_connection(addr: str):
    try:
        ssh_cli = paramiko.SSHClient()
        ssh_cli.connect(addr, username = "lvuser", password = "", timeout = 1)
        scp_cli = scp.SCPClient(ssh_cli.get_transport())
        print("Got connection successfully")
        return scp_cli, ssh_cli
    except TimeoutError:
        print("Connection timed out")
        return
    except:
        print("Error connecting")
        return

def upload_all(addr: str):
    saves = glob.glob("saves/*.json*")
    scp_cli = get_connection(addr)[0]
    if scp_cli == None:
        return
    for save in saves:
        scp_cli.put(save, remote_path = "/home/lvuser/deploy")
    print("Uploaded all save files")

def upload(addr: str, file_path: str):
    scp_cli = get_connection(addr)[0]
    if scp_cli == None:
        return
    scp_cli.put(file_path, remote_path = "/home/lvuser/deploy")
    print("Uploaded save successfully")

def download_all(addr: str):
    conns = get_connection(addr)
    scp_cli = conns[0]
    ssh_cli = conns[1]
    sftp = ssh_cli.open_sftp()
    remote_saves = sftp.listdir("/home/lvuser/deploy")
    for rs in remote_saves:
        if rs.endswith(".json"):
            scp_cli.get(remote_path = f"/home/lvuser/deploy/{rs}", local_path = "saves/")
    print("Downloaded all saves successfully")


def save_path(key_points: list, sample_rate: float, folder_path: str, file_name: str):
    data = {}
    data["meta_data"] = {
        "path_name": file_name,
        "sample_rate": sample_rate
    }
    data["key_points"] = [p.to_json() for p in key_points]
    interp_points = generateSplines.generateSplineCurves([[p.index, p.x, p.y, p.angle] for p in key_points])
    data["sampled_points"] = [[interp_points[0][i], interp_points[1][i], interp_points[2][i], interp_points[3][i]] for i in range(len(interp_points[0]))]
    try:
        out_file = open(f"{folder_path}\\{file_name}.json", "w")
        json.dump(data, out_file, indent = 2)
        out_file.close()
        print("Path saved successfully")
    except:
       print("Path was unable to be saved")

def load_path(file_path: str):
    try:
        with open(file_path) as json_save:
            data = json.load(json_save)
            key_points = []
            for p in data["key_points"]:
                key_points.append(Point(p["index"], p["delta_time"], p["x"], p["y"], p["angle"]))
            print("Path loaded successfully")
            return key_points, data["meta_data"]["sample_rate"], data["meta_data"]["path_name"]
    except:
        print("Path was unable to be loaded")
        return [], 0.01