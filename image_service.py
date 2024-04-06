import os
from datetime import datetime

def get_images_taken_on_date(directory_path, target_date):
    image_names = []
    if not os.path.isdir(directory_path):
        print("Directory does not exist.")
        return image_names

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                date_str = filename[:10]
                image_date = datetime.strptime(date_str, '%Y-%m-%d')
                if image_date.date() == target_date.date():
                    image_names.append(filename)
            except ValueError:
                continue
    return image_names


directory_path = '/images/'
target_date = datetime(2024, 4, 5)

images_on_date = get_images_taken_on_date(directory_path, target_date)
print("Images taken on", target_date.strftime('%Y-%m-%d'), ":", images_on_date)