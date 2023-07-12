import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

st.set_page_config(
    page_title="搜索歌曲",
    page_icon="🔎"
)

def chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option(
    #     "prefs", {"profile.managed_default_content_settings.images": 2}, # 默认图片不加载
    # )
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options)
    return driver

def search(keyword:str, filter:int, page:int) -> list:
    # filter 1:原唱/2:翻唱
    url = "http://search.5sing.kugou.com/home/json?keyword={}&sort=1&page={}&filter={}&type=0".format(keyword.lstrip().rstrip(), page, filter)
    resp = requests.get(url)
    return resp.json()

def crawl(url:str):
    driver = chrome_driver()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    r = soup.select_one("audio")
    try:
        src = r.attrs["src"]
    except:
        return None
    return src

search_keyword = st.text_input("关键字:").lstrip().rstrip()
search_filter_options = ["原唱", "翻唱"]
search_filter = st.radio(
    label="筛选:",
    options=search_filter_options
)

search_btn = st.button(label="搜索", disabled=False if search_keyword else True, use_container_width= True)
if search_btn and search_keyword != "":
    with st.spinner('搜索中, 请勿刷新页面...'):
        info_list = []
        for page in range(1, 3):
            resp = search(search_keyword, search_filter_options.index(search_filter)+1, 1)
            info_list.extend(resp["list"])
            if resp["pageInfo"]["totalPages"] == 1:
                break

    with st.spinner('解析中, 请勿刷新页面...'):        
        search_result_length = len(info_list)
        step = int(100 / search_result_length)
        progress_bar = st.progress(0, text="总计{}".format(search_result_length))
        for i, item in enumerate(info_list):
            url = crawl(item["songurl"])
            if url:
                st.write(item["originSinger"], help=item["songurl"])
                st.audio(data=url, format="audio/mp3", start_time=0)
                current_progress = 100 if i == search_result_length - 1 else  i * step + step
                progress_bar.progress(current_progress, text="进度: {}/{}".format(i+1, search_result_length))
        st.success("解析完成!")