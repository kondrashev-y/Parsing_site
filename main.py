import json
import os
import time
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml:q=0.9,image/avif,image/webp,image/apng,'
              '*/*:q=0.8'
}


def get_data(headers) -> str:
    """Collect data and return a JSON file"""

    # url = "https://www.landingfolio.com/"
    #
    # r = requests.get(url=url, headers=headers)
    #
    # with open('index.html', 'w') as file:
    #     file.write(r.text)

    offset = 0
    img_count = 0
    result_list = []

    while True:
        url = f'https://s1.landingfolio.com/api/v1/inspiration/?offset={offset}&color=%23undefined'

        response = requests.get(url=url, headers=headers)
        data = response.json()

        for item in data:
            if 'description' in item:

                images = item.get('images')

                for img in images:
                    img.update({'url': f'https://landingfoliocom.imgix.net/{img.get("url")}'})
                    img_count += 1

                result_list.append(
                    {
                        'title': item.get('title'),
                        'description': item.get('description'),
                        'url': item.get('url'),
                        'images': images
                    }
                )
            else:
                with open('result_list.json', 'a') as file:
                    json.dump(result_list, file, indent=4, ensure_ascii=False)

                return f'[INFO] Work finished. Images count is: {img_count}\n{"=" * 20}'

        print(f'[+] Processed {offset}')
        offset += 1


def download_imgs(file_path: str) -> str:
    """Download images"""
    try:
        with open(file_path, 'r') as file:
            src = json.load(file)
    except Exception as _ex:
        print(_ex)
        return '[INFO] Check the file path!'

    count = 1
    items_len = len(src)

    for item in src[:10]:
        item_name = item.get('title')
        item_img = item.get('images')

        if not os.path.exists(f'data/{item_name}'):
            os.mkdir(f'data/{item_name}')

        for img in item_img:
            r = requests.get(url=img['url'])

            with open(f'data/{item_name}/{img["type"]}.png', 'wb') as file:
                file.write(r.content)

        print(f'[+] Download {count}/{items_len}')
        count += 1

    return '[INFO] Work finished!'


def main():
    start_time = time.time()
    # print(get_data(headers=headers))
    print(download_imgs('result_list.json'))

    finished_time = time.time() - start_time

    print(f'Time of work: {finished_time}')


if __name__ == '__main__':
    main()