"""Example code for uploading images to image URL."""

import requests


def get_image_url(picture_path: str) -> str:
    """
    Given a file path, upload it to the cloud and then return the image URL corresponding to that image.

    Preconditions:
    - picture_path leads to a valid image picture
    - picture_path[-3:] == 'jpg'
    """
    # API key
    headers = {
        'Content-Type': 'image/jpeg',
        'Authorization': 'Bearer public_kW15ax2CzFC2twZcwg849iMndxSY',
    }

    # put picture location here
    with open(picture_path, 'rb') as f:
        data = f.read()

    response = requests.post('https://api.upload.io/v2/accounts/kW15ax2/uploads/binary', headers=headers, data=data)
    return response.json()["fileUrl"]


# TESTING FUNCTION HERE

# print(get_image_url('test_pictures/palm-tree.jpg'))
