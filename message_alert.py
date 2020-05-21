import requests, json, time, mimetypes
from requests_toolbelt.multipart.encoder import MultipartEncoder


mobile_number = "+8801686641190"

# Connector secret
application_secret = "URLA73LIW4"

# Connector ID
application_id = "b27f693c-f639-43de-aa6e-3c86a085eb4a"

# Kaizala Group ID
group_id_1 = "dc959f3d-7c3a-4a66-9a95-afa0ef048023@3"
group_id_2 = "329d5eac-addb-4ca2-9621-99b780ab0685@3"


SUPPORTED_MEDIA = {
    'Document': ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf'],
    'Image': ['jpg', 'jpeg', 'png'],
    'Album': ['jpg', 'jpeg', 'png'],
    'Audio': ['mp3', 'wav'],
    'Video': ['mp4', '3gp']
}


def generate_pin():
    url = "https://api.kaiza.la/v1/generatePin"

    payload = {
        'mobileNumber': mobile_number,
        'applicationId': application_id
    }

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    
    response = requests.request("POST", url, data=str(payload), headers=headers)

    if response.status_code == 200:
        print("OTP sent successfully!")
    else:
        print("OTP could not be sent! Try again!")


def login_with_pin_and_application_id(pin_code):
    url = "https://api.kaiza.la/v1/loginWithPinAndApplicationId"
    
    payload = {
        'mobileNumber': mobile_number,
        'applicationId': application_id,
        'applicationSecret': application_secret,
        'pin': pin_code
    }
    
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    
    response = requests.request("POST", url, data=str(payload), headers=headers)

    if response.status_code == 200:
        print("Refresh token generated successfully!")
        with open('refreshtoken.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4)
            print("Refresh token saved successfully!")


def load_refresh_token():
    try:
        with open('refreshtoken.json') as f:
            ref_token = json.load(f)
            print("Refresh token loaded successfully!")
    except:
        print("Refresh token isn't found!")
    
    return ref_token["refreshToken"]


def access_token(refresh_token):
    response = None
    current_time = int(round((time.time()-600) * 1000))

    try:
        with open('accesstoken.json') as f:
            response = json.load(f)
            print("Access token loaded successfully!")
    except:
        print("Access token isn't found!")
    
    if response and response["accessTokenExpiry"]>current_time:
        return response
    else:
        url = "https://api.kaiza.la/v1/accessToken"
        payload = ""
        headers = {
            'applicationId': application_id,
            'applicationSecret': application_secret,
            'refreshToken': refresh_token,
            'cache-control': "no-cache"
        }
        
        response = requests.request("GET", url, data=payload, headers=headers)

        if response.status_code == 200:
            print("Access token created successfully!")
            with open('accesstoken.json', 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, indent=4)
                print("Access token saved successfully!")
        else:
            print("Error! Access token could not be created successfully!")
        
        return response.json()


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


def send_media(end_point_url, group_id, acc_token, file_name, file_caption):
    # Step 1: upload the media file to a repository using the /media endpoint
    url = end_point_url + "/v1/media"
    content_type = mimetypes.guess_type(file_name)[0]
    action_type = determine_actionary_type(file_name)

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


if __name__ == "__main__":
    # Step 1: To generate OTP
    # generate_pin()

    # Step 2: Set the pin_code value as OTP code and generate Refresh_Token
    # login_with_pin_and_application_id(pin_code=252673)

    # load refresh token and access token
    refresh_token = load_refresh_token()
    response = access_token(refresh_token)

    # interact with Kaizala app
    if response and response["accessToken"]:
        acc_token = response["accessToken"]
        end_point_url = response["endpointUrl"]

        # Messages and multiple files are being sent to several Kaizala groups at the same time 
        # Sent a message
        message = "Hello! This message sent automatically through Kaizala API!"
        send_message(end_point_url, group_id_1, acc_token, message)

        # Sent an audio file
        send_media(end_point_url, group_id_1, acc_token, "ringtone.mp3", "Iphone Ringtone!")

        # Sent an image
        send_media(end_point_url, group_id_2, acc_token, "robi.png", "Robi Logo!")

        # Sent a pdf
        send_media(end_point_url, group_id_2, acc_token, "book.pdf", "It's a classic poetry book!")
    else:
        print("Server Down!")
    