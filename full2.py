import os
import re
import random
import requests
from bs4 import BeautifulSoup
import json

# Tạo thư mục nếu nó chưa tồn tại
j = 1
if not os.path.exists('nhot'):
    os.makedirs('nhot')

data_list = []
for i in range(1, 2):

    url = f'https://shop2banh.vn/nhot-xe-may/trang-{i}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    div_items = soup.find_all(
        'div', {'class': 'col-lg-4 col-md-6 col-sm-4 col-xs-6 items ripple'})
    for div_item in div_items:
        a_tag = div_item.find('a')
        if a_tag is not None:
            href = a_tag.get('href')
            if href is not None:
                img_tag = div_item.find('img')
                if img_tag is not None:
                    if 'data-src' in img_tag.attrs:
                        src = img_tag['data-src']
                    else:
                        src = img_tag['src']
                    if src is not None:
                        img_ext = src.split('.')[-1]
                        img_name = f"{j}.{img_ext}"
                        j += 1
                        img_path = os.path.join('nhot', img_name)
                        with open(img_path, 'wb') as f:
                            f.write(requests.get(src).content)
                            print(img_name)

                # Lấy thông tin sản phẩm và lưu vào danh sách data_list
                detail_page = requests.get(href)
                detail_soup = BeautifulSoup(detail_page.content, 'html.parser')
                detail_div = detail_soup.find(
                    'div', {'class': 'col-lg-9 col-md-9 col-sm-12 col-xs-12 col-left-ct'})
                if detail_div is not None:
                    title = detail_div.find('h1').text.strip()
                    img_url = src if src is not None else ''
                    description_div = detail_div.find(
                        'div', {'class': 'description-detail'})
                    description = description_div.get_text(
                        separator=' ').strip() if description_div is not None else ''
                    span_tags = detail_div.find('div', {'class': 'price'})
                    prices = span_tags.find_all('span')
                    lsPrice = []
                    for a in prices:
                        price = a.text.strip()
                        lsPrice.append(price)

                    data_list.append(
                        {'name': title, 'description': description, 'price': lsPrice[0], 'img_url': img_name})

# Lưu danh sách vào file data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False)

# Lưu danh sách ảnh vào file images.txt
with open('images.txt', 'w') as f:
    for i in range(1, j):
        img_name = f"{i}.jpg"
        img_path = os.path.join('nhot', img_name)
        f.write(f"{img_path}\n")


def convert_price(price_str):
    # tìm và loại bỏ các ký tự không cần thiết trong chuỗi giá trị
    price_str = re.sub(r'[^\d]+', '', price_str)
    # chuyển đổi chuỗi giá trị thành số
    if price_str.isdigit():
        return int(price_str)
    else:
        return 0


with open('nhot.txt', 'w') as f:
    o = 1
    h = 'PC'
    for data in data_list:
        if o < 10:
            h = h + '0'+str(o)
        else:
            h += str(o)
        sl = random.randint(100, 900)
        name = data['name']
        number = sl
        price = data['price'].lower()  # random.randint(50, 300) * 1000
        if price == 'hết hàng':
            price = 0
            number = 0
        else:
            price = convert_price(price)

        like = random.randint(0, 10)
        image = data['img_url']
        # print(data['img_url'][0])
        # print(image + 'abc')
        description = data['description'].replace('\r\n', ' ')

        data_str = (f'[ "name"=>"{name}", '
                    f'"number" => {number}, '
                    f'"price" => {price}, '
                    f'"like" => {like}, '
                    f'"product_code" => {h}, '
                    f'"image"=>"nhot/{image}", '
                    f'"description"=>"{description}" ],\n')
        h = 'PC'
        o += 1
        f.write(data_str)
