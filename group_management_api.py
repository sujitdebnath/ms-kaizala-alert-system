from packages_and_others import *
from authentication_api import *


def get_members(end_point_url, acc_token, group_id):
    url = end_point_url + "/v1/groups/" + group_id + "/members"

    headers = {
        'accessToken': acc_token,
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)

    if response.status_code == 200:
        print("Group info extracted successfully!")
    else:
        print("Group info could not be extracted successfully!")
    
    return response.json()

def add_members(end_point_url, acc_token, group_id, phone_numbers):
    url = end_point_url + "/v1/groups/" + group_id + "/members"

    payload = {
        'members': phone_numbers
    }

    headers = {
        'accessToken': acc_token,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("PUT", url, data=str(payload), headers=headers)
    print(response.text)

    if response.status_code == 200:
        print("Memebers added successfully!")
    else:
        print("Memebers could not be added successfully!")


def remove_members(end_point_url, acc_token, group_id, user_id):
    url = end_point_url + "/v1/groups/" + group_id + "/members/" + user_id

    headers = {
        'accessToken': acc_token,
        'cache-control': "no-cache"
    }

    response = requests.request("DELETE", url, headers=headers)
    print(response.text)

    if response.status_code == 200:
        print("Memebers removed successfully!")
    else:
        print("Memebers could not be removed successfully!")
