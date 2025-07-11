import utils
import output_ui
import requests as req
from sbid_headers import *
from bs4 import BeautifulSoup as bs

def dl(img_num: int, url: str, directory: str, mode: str):
    domain = 'https://www.nogizaka46.com'
    dl_count = 0
    while True:
        page_detail = req.get(url, timeout=60, headers=headers)
        source = bs(page_detail.content, "html.parser")
        images = source.select('div.bd--edit')[0].select('img')
        for img in images:
            imglink = img.attrs.get("src")
            if imglink.endswith("jpg") or imglink.endswith("png"):
                file_type = imglink[imglink.rfind("."):]
                imgurl = domain + imglink
                retry_count = 0
                max_retries = 10
                while retry_count < max_retries:
                    try:
                        response = req.head(imgurl, timeout=60)
                        if response.status_code == 200:
                            imgdl = req.get(imgurl).content
                            filename = utils.concat_dir(directory=directory) + '/' + str(img_num) + file_type
                            output_ui.insert_msg(f'{filename} {imgurl} \n')
                            img_num += 1
                            dl_count += 1
                            with open(filename, mode='wb') as f:
                                f.write(imgdl)
                            break
                    except (req.ConnectionError, req.Timeout) as e:
                        retry_count += 1
            elif not imglink:
                break
            elif imglink is None or imglink == "":
                continue
        if mode == 'single':
            break
        else:
            try:
                next_page_link = source.select('div.bd--hn__pn._n a')[0]['href']
            except Exception:
                break
            url = domain + next_page_link
    bid = source.select('div.bd--cmt__in.js-apicomment')[0]['data-api'][source.select('div.bd--cmt__in.js-apicomment')[0]['data-api'].rfind('=')+1:]
    img_num -= 1
    return bid, directory, img_num, dl_count