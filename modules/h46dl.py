import utils
import output_ui
import requests as req
from sbid_headers import *
from bs4 import BeautifulSoup as bs

def dl(img_num: int, url: str, directory: str, mode: str):
    domain = 'https://www.hinatazaka46.com'
    dl_count = 0
    while True:
        page_detail = req.get(url, timeout=60, headers=headers)
        source = bs(page_detail.content, "html.parser")
        images = source.select('div.p-blog-article')[0].select('img')
        for img in images:
            imgurl = img.attrs.get("src")
            if imgurl is None or imgurl == "" or not imgurl.endswith("jpg") or not imgurl.endswith("png"):
                continue
            retry_count = 0
            max_retries = 10
            file_type = imgurl[imgurl.rfind("."):]
            while retry_count < max_retries:
                try:
                    response = req.head(imgurl, timeout=60)
                    if response.status_code == 200:
                        imgdl = req.get(imgurl, headers=headers).content
                        filename = utils.concat_dir(directory=directory) + '/' + str(img_num) + file_type
                        output_ui.insert_msg(f'{filename} {imgurl} \n')
                        img_num += 1
                        dl_count += 1
                        with open(filename, mode='wb') as f:
                            f.write(imgdl)
                        break
                except (req.ConnectionError, req.Timeout) as e:
                    retry_count += 1
        if mode == 'single':
            break
        else:
            next_page = source.select('div.c-pager__item.c-pager__item--next.c-pager__item--kiji.c-pager__item--kiji__blog > a')
            if not next_page:
                break
            for link in next_page:
                next_page_link = link['href']
                url = domain + next_page_link
    bid = source.find('meta', attrs={'property': 'og:url'}).get('content')\
        [source.find('meta', attrs={'property': 'og:url'}).get('content').rfind('/')+1:source.find('meta', attrs={'property': 'og:url'}).get('content').rfind('?')]
    img_num -= 1
    return bid, directory, img_num, dl_count