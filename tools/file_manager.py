import json
import glob
from . import convert
import paramiko
import scp

from data_assets.point import Point
from SplineGeneration import generateSplines

def get_connection(addr: str):
    print("Connecting...")
    try:
        ssh_cli = paramiko.SSHClient()
        ssh_cli.load_system_host_keys()
        ssh_cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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
    print("Uploading...")
    saves = glob.glob("saves/*.json*")
    conns = get_connection(addr)
    if conns == None:
        return False
    scp_cli = conns[0]
    for save in saves:
        scp_cli.put(save, remote_path = "/home/lvuser/deploy")
    print("Uploaded all save files")
    return True

def upload(addr: str, file_path: str):
    print("Uploading all...")
    conns = get_connection(addr)
    if conns == None:
        return False
    scp_cli = conns[0]
    scp_cli.put(file_path, remote_path = "/home/lvuser/deploy")
    print("Uploaded save successfully")
    return True

def download_all(addr: str):
    print("downloading all...")
    conns = get_connection(addr)
    if conns == None:
        return False
    scp_cli = conns[0]
    ssh_cli = conns[1]
    sftp = ssh_cli.open_sftp()
    remote_saves = sftp.listdir("/home/lvuser/deploy")
    for rs in remote_saves:
        if rs.endswith(".json"):
            scp_cli.get(remote_path = f"/home/lvuser/deploy/{rs}", local_path = "saves/")
    print("Downloaded all saves successfully")
    return True


def save_path(key_points: list[Point], sample_rate: float, folder_path: str, file_name: str):
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
        return True
    except:
       print("Path was unable to be saved")
       return False

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
        return [], 0.01, ""