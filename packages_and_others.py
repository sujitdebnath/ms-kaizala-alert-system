import pandas as pd
# import excel2img, phonenumbers
import phonenumbers
import os, requests
import re, json, time, mimetypes
from PIL import Image, ImageOps
from datetime import date, timedelta
from requests_toolbelt.multipart.encoder import MultipartEncoder


# Connector's mobile number
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
    'Video': ['mp4', '3gpp']
}


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
