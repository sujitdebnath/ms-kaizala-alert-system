from os import getcwd
from packages_and_others import *
from authentication_api import *
from content_creation_api import *
from group_management_api import *


group_id = group_id_2


if __name__ == "__main__":
    authentication = retrieve_authentication()

    if authentication == None:
        print("Authentication Failed! Server Down!")
    else:
        acc_token, end_point_url = authentication

        send_message(end_point_url, group_id, acc_token, "Hello From Kaizala Message Alert System!\nThis is an automatic message please ignore!")

        image_path = "Voice Traffic.png"
        caption = "Voice Traffic"
        send_media(end_point_url, group_id, acc_token, image_path, caption)

        # abs_path = os.path.join(os.getcwd(), "images")
        # images = [image for image in os.listdir(abs_path) if os.path.isfile(os.path.join(abs_path, image))]
        
        # for image in images:
        #     image_path = os.path.join(abs_path, image)
        #     caption = image
        #     send_media(end_point_url, group_id, acc_token, image_path, caption)


        # files = [file for file in os.listdir() if os.path.isfile(os.path.join(os.getcwd(), file))]

        # for file in files:
        #     filename, file_extension = os.path.splitext(file)

        #     if file_extension not in ('.json', '.py', '.txt', '.zip'):
        #         file_path = os.path.join(os.getcwd(), file)
        #         caption = filename
        #         print(file_path)
        #         send_media(end_point_url, group_id, acc_token, file_path, caption)