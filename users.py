import json
import os

VIP_FILE = "vip_users.json"

if not os.path.exists(VIP_FILE):
    with open(VIP_FILE, "w") as f:
        json.dump([], f)

def is_vip(user_id):
    with open(VIP_FILE) as f:
        vip_list = json.load(f)
    return str(user_id) in vip_list

def add_vip_user(user_id):
    with open(VIP_FILE) as f:
        vip_list = json.load(f)
    if str(user_id) not in vip_list:
        vip_list.append(str(user_id))
        with open(VIP_FILE, "w") as f:
            json.dump(vip_list, f)

def remove_vip_user(user_id):
    with open(VIP_FILE) as f:
        vip_list = json.load(f)
    if str(user_id) in vip_list:
        vip_list.remove(str(user_id))
        with open(VIP_FILE, "w") as f:
            json.dump(vip_list, f)

def list_users():
    with open(VIP_FILE) as f:
        vip_list = json.load(f)
    return ["@everyone"], [f"<@{u}>" for u in vip_list]
