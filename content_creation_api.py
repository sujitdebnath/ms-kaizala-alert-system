from packages_and_others import *
from authentication_api import *


def send_message(end_point_url, group_id, acc_token, message):
    url = end_point_url + "/v1/groups/" + group_id + "/messages"
    
    payload = {
        'message': message
    }

    headers = {
        'accessToken': acc_token,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=str(payload), headers=headers)
    print(response.text)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Message could not be sent successfully!")


def determine_actionary_type(file_name):
    split_content = file_name.split('.')

    if len(split_content) != 2:
        print("Invalid file or file name!")
        return None
    
    for actionType in SUPPORTED_MEDIA:
        ext = SUPPORTED_MEDIA.get(actionType, [])
        if split_content[1] in ext:
            return actionType
    return None


def upload_media(end_point_url, acc_token, file_name):
    url = end_point_url + "/v1/media"
    content_type = mimetypes.guess_type(file_name)[0]
    action_type = determine_actionary_type(file_name)

    print("url: {}".format(url))
    print("content type: {}, action type: {}".format(content_type, action_type))

    if action_type == None:
        print('Unsupported file!')
        return

    fileEncoder = MultipartEncoder(
        fields = {
            'files':(file_name, open(file_name,'rb'), content_type)
        }
    )

    headers = {
        'accessToken': acc_token,
        'Content-Type': fileEncoder.content_type,
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=fileEncoder, headers=headers)

    if response.status_code == 200:
        print("Media uploaded successfully!")
    else:
        print("Media could not be uploaded successfully!")
    
    return response


def send_media(end_point_url, group_id, acc_token, file_name, file_caption):
    # Step 1: upload the media file to a repository using the /media endpoint
    action_type = determine_actionary_type(file_name)
    response = upload_media(end_point_url, acc_token, file_name)
    # Step 1: End

    # Step 2: use the resource URL to post as an Action inside Kaizala
    url = end_point_url + "/v1/groups/" + group_id + "/actions"
    response = response.json()
    media_resource = response["mediaResource"]

    payload = {
        'actionType': action_type,
        'actionBody': {
            'caption': file_caption,
            'mediaResource': media_resource}
    }

    headers = {
        'accessToken': acc_token,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=str(payload), headers=headers)
    print(response.text)
    # Step 2: End

    if response.status_code == 200:
        print("Media sent successfully!")
    else:
        print("Media could not be sent successfully!")


def upload_multiple_media(end_point_url, acc_token, file_names):
    url = end_point_url + "/v1/media"
    content_type = mimetypes.guess_type(file_names[0])[0]
    action_type = determine_actionary_type(file_names[0])

    print("url: {}".format(url))
    print("content type: {}, action type: {}".format(content_type, action_type))

    if action_type == None:
        print('Unsupported file!')
        return

    fileEncoder = MultipartEncoder(
        fields = {
            'FileName'.join(str(ind)): (file_name, open(file_name,'rb'), content_type) for ind, file_name in enumerate(file_names, 1)
        }
    )

    headers = {
        'accessToken': acc_token,
        'Content-Type': fileEncoder.content_type,
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=fileEncoder, headers=headers)

    if response.status_code == 200:
        print("All the Media uploaded successfully!")
    else:
        print("Media could not be uploaded successfully!")
    
    return response


def send_album(end_point_url, group_id, acc_token, file_names, album_caption):
    # Step 1: upload the media file to a repository using the /media endpoint
    response = upload_multiple_media(end_point_url, acc_token, file_names)
    # Step 1: End

    # Step 2: use the resource URL to post as an Action inside Kaizala
    url = end_point_url + "/v1/groups/" + group_id + "/actions"
    response = response.json()
    media_resource = response["mediaResource"]

    payload = {
        'actionType': 'Album',
        'actionBody': {
            'caption': album_caption,
            'mediaResource': media_resource}
    }

    headers = {
        'accessToken': acc_token,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=str(payload), headers=headers)
    print(response.text)
    # Step 2: End

    if response.status_code == 200:
        print("Album sent successfully!")
    else:
        print("Album could not be sent successfully!")
