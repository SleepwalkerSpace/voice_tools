import os
import time

import streamlit as st

st.set_page_config(
    page_title="分离人声",
    page_icon="🎚️"
)

project_path = os.getcwd()
project_static_path = os.path.join(project_path, "static")

spleeter_path = os.path.join(
    os.path.abspath(os.path.join(os.getcwd(), "..")),
      "spleeter_venv", "Scripts", "spleeter.exe")

spleeter_out_path = os.path.join(project_static_path, "spleeter_out")

uploaded_file = st.file_uploader(
    label = "音频文件",
    type = ["MP3", "WAV"],
    help = ""
    )

if uploaded_file is not None:
    ns = str(time.time_ns())
    source_fn = "{}.{}".format(ns, os.path.splitext(uploaded_file.name)[-1][1:])
    source_path = os.path.join(project_static_path, source_fn)
    with open(source_path, "wb") as f:
        f.write(uploaded_file.getvalue())
        f.close()

    output_path = os.path.join(spleeter_out_path, ns, "accompaniment.mp3")

    cmd = "{} separate -p spleeter:2stems -c mp3 -o {} {}".format(
        spleeter_path, spleeter_out_path, source_path)

    with st.spinner('分离人声中, 请勿刷新页面...'):
        status = os.system(cmd)
        if status == 0:
            st.success("分离人声成功")
            st.audio(data=output_path, format="audio/mp3", start_time=0)
            if os.path.isfile(source_path):
                os.remove(source_path)

            with open(output_path, "rb") as file:
                st.download_button(
                    label = "下载伴奏",
                    data = file,
                    file_name = "spleeter_{}.mp3".format(os.path.splitext(uploaded_file.name)[0]),
                    mime = "audio/mp3"
                )

        else:
            st.warn("分离人声失败")
    