import requests
import json


access_token = ""
user_id =
token_yan = ""


def photo_write(data):
    with open("photos.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=2)
    return


def get_max_size(size):
    if size["width"] >= size["height"]:
        return size["width"]
    else:
        return size["height"]


def get_photos_info(filename, info):
    filename = filename + ".json"
    with open("D:\Home_work\Itog\Vk_photos\ " + filename, "w", encoding='utf-8') as file:
        json.dump(info, file, indent=2)
    return


def download_photo_vk(url, filename):
    r = requests.get(url, stream=True)
    with open("D:\Home_work\Itog\Vk_photos\ " + filename + ".jpeg", "bw") as file:
        for chunk in r.iter_content(4096):
            file.write(chunk)


def photo_from_vk(access_token, user_id):
    api = requests.get("https://api.vk.com/method/photos.get", params={
        "owner_id": user_id,
        "access_token": access_token,
        "album_id": "profile",
        "extended": 1,
        "photo_sizes": 0,
        "count": 5,
        "v": 5.131
    })
    photo_write(api.json())

    photos = json.load(open("photos.json"))["response"]
    photos_info = {"file_name": [], "size": []}
    for photo in photos["items"]:
        sizes = photo["sizes"]
        url_largest_photo = max(sizes, key=get_max_size)["url"]
        type_largest_photo = max(sizes, key=get_max_size)["type"]
        name = str(str(photo["likes"]["count"]) + "_" + str(photo["date"]))

        photos_info["file_name"].append(name)
        photos_info["size"].append(type_largest_photo)
        get_photos_info(name, photos_info)

        download_photo_vk(url_largest_photo, name)
    return photos_info


def yandex_load(filename, path, token_yan):
    URL = "https://cloud-api.yandex.net/v1/disk/resources/upload?path="+filename
    print(URL)
    headers = {
        "Accept": "application/json",
        "Authorization": f"OAuth {token_yan}",
    }
    upload_URL = (requests.get(URL, headers=headers)).json()['href']
    print(upload_URL)
    with open(path, "rb") as f:
        files = {"file": (filename, f)}
        response = requests.put(upload_URL, headers=headers, files=files)

    if response.status_code == 201:
        return
    else:
        raise Exception("Failed to upload file")


def upload_all_photos(photos_info, token_yan):
    for photo_name in photos_info["file_name"]:
        photo_name = photo_name + '.jpeg'
        path = "D:\Home_work\Itog\Vk_photos\ "+photo_name
        print(path)
        yandex_load(photo_name, path, token_yan)
    return


photos_info = photo_from_vk(access_token, user_id)
upload_all_photos(photos_info, token_yan)
