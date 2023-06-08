import os
import streamlit as st
from pydub import AudioSegment

project_path = os.getcwd()
project_static_path = os.path.join(project_path, "static")

st.set_page_config(
    page_title="升降伴奏",
    page_icon="🎼"
)

uploaded_file = st.file_uploader(
    label = "升降伴奏(目前仅限于MP3格式)",
    type = ["MP3"],
    help = "提交需要升降音阶的伴奏MP3文件"
    )

if uploaded_file is not None:
    source_path = os.path.join(project_static_path, uploaded_file.name)
    with open(source_path, "wb") as f:
        f.write(uploaded_file.getvalue())
        f.close()
    
    frame_rate = AudioSegment.from_mp3(source_path).frame_rate
    st.text("伴奏赫兹: {}".format(frame_rate))

    st.text("原调:")
    st.audio(data=uploaded_file, format="audio/mp3", start_time=0)

    level = st.slider(
    '调整音阶:',
    -12, 12, 0)
    level_str = ""
    if level < 0:
          level_str = str(level)
    else:
          level_str = "+"+str(level)

    source_fn, ext = os.path.splitext(uploaded_file.name)
    output_fn = "{}{}{}".format(source_fn, level_str, ext)
    output_path = os.path.join(project_static_path, output_fn)
    if os.path.isfile(output_path):
        os.remove(output_path)
    
    if st.button(
        label="生成伴奏: {}".format(level_str), disabled=True if level == 0 else False):
            with st.spinner('变调中, 请稍等...'):
                cmd = 'ffmpeg -i {} -filter_complex "asetrate={}*2^({}/12),atempo=1/2^({}/12)" {}'.format(
                source_path, frame_rate, level, level, output_path)
                status = os.system(cmd)

                if status == 0:
                    st.text("变调:")
                    st.audio(data=output_path, format="audio/mp3", start_time=0)

                    with open(output_path, "rb") as file:
                        st.download_button(
                            label = "下载变调伴奏",
                            data = file,
                            file_name = output_fn,
                            mime = "audio/mp3"
                        )

                else:
                     st.text("变调失败")

    if os.path.isfile(source_path):
        os.remove(source_path)