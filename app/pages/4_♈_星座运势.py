import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="星座运势",
    page_icon="♈"
)

constellations = [
    "♈白羊座[03/21-04/20]",
    "♉金牛座[04/21-05/21]",
    "♊双子座[05/22-06/21]",
    "♋巨蟹座[06/22-07/22]",
    "♌狮子座[07/23-08/23]",
    "♍处女座[08/24-09/23]",
    "♎天秤座[09/24-10/23]",
    "♏天蝎座[10/24-11/22]",
    "♐射手座[11/23-12/21]",
    "♑魔羯座[12/22-01/20]",
    "♒水瓶座[01/21-02/19]",
    "♓双鱼座[02/20-03/20]",
]

args = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]

constellation = st.selectbox(
    label="选择星座",
    options=constellations,
)

date_args = {
    "今日运势": 0,
    "明日运势": 1,
    "本周运势": 2,
    "本月运势": 3,
    "今年运势": 4,
    }

def get_fortune(constellation: int, date: int) -> str:
    url = "https://www.xzw.com/fortune/{}/{}.html".format(
        args[constellations.index(constellation)],
        date)
    res = requests.get(url)
    if res.status_code == 200:
        contents = BeautifulSoup(
            res.text, "lxml"
            ).select_one(
            "div[class='c_box'] div[class='c_cont']"
            ).decode_contents()
        return contents
    else:
        return ""

for date in date_args:
    st.subheader(date)
    st.write(get_fortune(constellation, date_args[date]), unsafe_allow_html=True)
    st.divider()