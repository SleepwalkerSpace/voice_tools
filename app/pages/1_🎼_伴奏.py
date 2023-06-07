import os

import streamlit as st
from pydub import AudioSegment

project_path = os.getcwd()
project_static_path = os.path.join(project_path, "static")

st.set_page_config(
    page_title="伴奏",
    page_icon="🎼"
)

uploaded_file = st.file_uploader(
    label = "升降伴奏",
    type = ["MP3"],
    help = "提交需要升降音阶的伴奏MP3文件."
    )

if uploaded_file is not None:
    source_path = os.path.join(project_static_path, uploaded_file.name)
    with open(source_path, "wb") as f:
        f.write(uploaded_file.getvalue())
        f.close()
    
    st.text("存放路径: {}".format(source_path))
    frame_rate = AudioSegment.from_mp3(source_path).frame_rate
    st.text("伴奏赫兹: {}".format(frame_rate))

    st.text("原调:")
    st.audio(uploaded_file)

    level = st.slider(
    '调整音阶:',
    -12, 12, 0)
    level_str = ""
    if level < 0:
          level_str = str(level)
    else:
          level_str = "+"+str(level)

    fn, ext = os.path.splitext(uploaded_file.name)
    output_path = os.path.join(project_static_path, "{}{}{}".format(fn, level_str, ext))

    if st.button(
        label="生成伴奏: {}".format(level_str), disabled=True if level == 0 else False):
            with st.spinner('变调中, 请稍等...'):
                status = os.system("ffmpeg -i '{}' -filter_complex 'asetrate={}*2^({}/12),atempo=1/2^({}/12)' {}".format(
                source_path, frame_rate, level, level, output_path))
                
                if status == 0:
                    st.balloons()

                    st.text("变调:")
                    st.audio(output_path)