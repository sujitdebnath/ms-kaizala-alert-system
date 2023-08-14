from packages_and_others import *


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
        print("Access token has expired or token hasn't been found! Need a new token!")

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


def retrieve_authentication():
    refresh_token = load_refresh_token()
    response = access_token(refresh_token)

    if response and response["accessToken"]:
        acc_token = response["accessToken"]
        end_point_url = response["endpointUrl"]
        return acc_token, end_point_url
    else:
        return None
