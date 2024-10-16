import os


def save_image(image_data, image_path):

    os.makedirs(image_path, exist_ok=True)

    with open(image_path, 'wb') as f:
        f.write(image_data)
