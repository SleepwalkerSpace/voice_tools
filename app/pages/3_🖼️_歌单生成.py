import os
import time
from string import punctuation as en_punctuation
from zhon.hanzi import punctuation as zh_punctuation

import streamlit as st
from PIL import Image, ImageFont, ImageDraw, ImageFilter

project_path = os.getcwd()
project_static_path = os.path.join(project_path, "static")
project_static_fonts = os.path.join(project_static_path, "fonts")

st.set_page_config(
    page_title="歌单生成",
    page_icon="🖼️"
)

class SongListCards():
    """ 歌单图片生成
    """
    def __init__(self,
        song_list: list,   # 文本列表
        card_nums: int,    # 图卡数量
        background: str|bytes,    # 背景图片路径
        font_path: str,    # 字体路径
        font_fill: str,    # 字体颜色
        font_size: int,    # 字体颜色
        c_interval: int,   # 列间距
        r_interval: int,   # 行间距
        background_blur: bool, # 背景图片模糊
        security_watermark: bool,   # 防盗水印
        ):
    
        self.song_list = sorted(song_list, key=self.length)
        self.card_nums = card_nums
        # 加载背景图片
        if background is not None:
            # self.background = Image.open(background)
            if isinstance(background, str):
                try:
                    self.background = Image.open(background)
                except:
                    pass
            else:
                self.background = background
        
        # 虚化背景 
        if background_blur:
            self.background = self.background.filter(ImageFilter.BLUR)

        # 字体路径
        self.font_path = font_path
        # 字体颜色
        self.font_fill = font_fill
        # 字体大小
        self.font_size = font_size

        # 水印
        self.security_watermark = security_watermark
        # 原卡尺寸
        self.origin_card_wide, self.origin_card_high = self.background.size
        # 单卡宽度
        self.single_card_wide = self.origin_card_wide / self.card_nums
        # 单卡高度
        self.single_card_high = self.origin_card_high   
        # 间距 - 边框左右 
        self.wide_border_interval = self.single_card_wide * 0.03
        # 间距 - 边框上下
        self.high_border_interval = self.single_card_high * 0.03
        # 间距 - 列之间
        self.c_interval = c_interval
        # 间距 - 行之间
        self.r_interval = r_interval
        # 行数
        self.row_num = int((self.single_card_wide - self.wide_border_interval * 2) / self.font_size)
        self.consume=0
    @staticmethod
    def length(text: str) -> int:
        l = 0
        for t in text:
            if t.isspace():
                l += 1
            elif t in en_punctuation or t in zh_punctuation:
                l += 1
            elif t.encode("UTF-8").isalpha():
                l += 1
            else:
                l += 2
        return l // 2
    
    def generate(self):
        r_wide = self.single_card_wide - self.wide_border_interval * 2
        column_num = 0
        column_infos = {}
        while True:
            try:
                column = self.song_list[column_num * self.row_num: column_num * self.row_num + self.row_num]
            except:
                column = self.song_list[column_num * self.row_num:]
            
            max_length = 0
            for item in column:
                if self.length(item) > max_length:
                    max_length = self.length(item)
            if r_wide - (max_length * self.font_size) <= 0:
                break
            else:
                column_infos[column_num] = {
                    "max_length": max_length,
                }
                r_wide -= (max_length * self.font_size) + self.font_size
                column_num += 1
        card = self.background.copy()
        i = 0
        for c in range(column_num):
            for r in range(self.row_num):
                if i+1 >= len(self.song_list):
                    self.consume += i+1
                    return card

                before = 0
                if c > 0:
                    for bc in range(c):
                        before += column_infos[bc]["max_length"]
                
                text = self.song_list[i]
                x = self.wide_border_interval*2 + (self.font_size * before) + self.font_size * c + (r_wide / column_num * c)
                x += (column_infos[c]["max_length"] - self.length(text)) * self.font_size / 2
                y = self.high_border_interval + self.font_size * r  
                ImageDraw.Draw(card).text(
                    xy=(x, y),
                    text=text,
                    fill=font_fill,
                    font=ImageFont.truetype(font_path, font_size))
                i += 1
        self.consume += i+1
        return card

st.write("1.新建文本文件(txt格式)")
st.write("2.编辑文件每行为一首歌")
st.text_area(label="文件内容示例",
             value="示例歌曲001\n示例歌曲002\n示例歌曲003\n....\n示例歌曲xxx", 
             height=140,
             disabled=True)
st.write("3.在下面上传文本文件")
song_list_file = st.file_uploader(
    label = "歌单文件(仅限于TXT格式)",
    type = ["TXT"])

if song_list_file is not None:
    song_list = []
    for i, item in enumerate(song_list_file.read().splitlines()):
        song_list.append(item.decode("UTF-8").strip().capitalize())
    st.session_state["song_list"] = song_list
    st.success("文件上传成功, 共计{}行.".format(len(song_list)))

st.divider()

st.write("4.选择文字大小和文字颜色(可实时调整)")
font_path = os.path.join(project_static_fonts, "default.ttf")
font_setting_1, font_setting_2 = st.columns(2)
with font_setting_1:
    font_fill = st.color_picker('选择字体颜色', '#FFFFFF')
with font_setting_2:
    font_size = st.slider("选择字体大小", min_value=10, max_value=100, value=26)

interval_setting_1, interval_setting_2  = st.columns(2)
with interval_setting_1:
    c_interval = st.slider("列间距", min_value=font_size, max_value=1000, value=font_size, disabled=True)
with interval_setting_2:
    r_interval = st.slider("行间距", min_value=0, max_value=font_size, value=0, disabled=True)

st.divider()
st.write("5.在下面上传背景图片")
bg_file = st.file_uploader(
    label = "背景图片",
    type = ["PNG", "JPEG"])

if bg_file is not None:
    st.success("背景图片上传成功")

st.divider()
st.write("6.右键图片另存为即可")
if song_list_file is not None and bg_file is not None:
    bg = Image.open(bg_file)
    t = len(st.session_state["song_list"])
    r = 0
    while True:
        imp = SongListCards(
                song_list=st.session_state["song_list"][r:],
                card_nums=1,
                background=bg,
                font_path=font_path,
                font_fill=font_fill,
                font_size=font_size,
                c_interval=c_interval,
                r_interval=r_interval,
                background_blur=False,
                security_watermark=False,
            )
        card = imp.generate()
        r += imp.consume
        st.image(card)
        if r == t:
            break