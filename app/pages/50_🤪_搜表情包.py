import streamlit as st
import requests
from urllib.parse import urljoin 

st.set_page_config(
    page_title="搜表情包",
    page_icon="🤪"
)

def search(keyword:str, star:int):
    url = "https://www.dbbqb.com/api/search/json?start={}&w={}".format(star, keyword)
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "Web-Agent":"web",
    }
    res = []
    try:
        res = requests.get(url, headers=headers).json()

    except:
        pass
    
    return res

search_keyword = st.text_input("表情包关键字:")
search_btn = st.button(label="搜索", disabled=False if search_keyword else True, use_container_width= True)
if search_btn:
    image_list = []
    for star in range(0, 200, 100):
        contexts = search(search_keyword, star)
        if len(contexts) == 0:
            break
        for item in contexts:                                    
            path = urljoin("https://image.dbbqb.com", item["path"])
            image_list.append(urljoin(path, item["hashId"]))
    
    if len(image_list):
        st.image(image_list, width=100)
    else:
        st.warning("今日已达到次数限制")