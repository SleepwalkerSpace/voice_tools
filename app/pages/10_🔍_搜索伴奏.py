import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

st.set_page_config(
    page_title="搜索伴奏",
    page_icon="🔍"
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

def search(keyword:str) -> list:
    url = "http://search.5sing.kugou.com/home/json?keyword={}&sort=1&page=1&filter=3&type=0".format(keyword.lstrip().rstrip())
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

search_keyword = st.text_input("关键字:")
search_btn = st.button(label="搜索", disabled=False if search_keyword else True, use_container_width= True)
if search_btn:
    with st.spinner('搜索中, 请勿刷新页面...'):
        search_result = search(search_keyword)
        if search_result:
            st.success("搜索完成!")
        else:
            st.error("搜索失败!")

    with st.spinner('解析中, 请勿刷新页面...'):
        search_result_length = len(search_result["list"])
        step = int(100 / search_result_length)
        progress_bar = st.progress(0, text="总计{}".format(search_result_length))
        for i, item in enumerate(search_result["list"]):
            st.write(item["originSinger"], item["songurl"])
            url = crawl(item["songurl"])
            if url:
                st.text(item["originSinger"])
                st.audio(data=url, format="audio/mp3", start_time=0)
                current_progress = 100 if i == search_result_length - 1 else  i * step + step
                progress_bar.progress(current_progress, text="进度: {}/{}".format(i+1, search_result_length))
        st.success("解析完成!")

# crawl_url = st.text_input("5SingURL")
# if st.button("creaw"):
#     url = crawl(crawl_url)
#     st.audio(data=url, format="audio/mp3", start_time=0)