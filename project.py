import streamlit as st
import numpy as np
from PIL import Image
import cv2
import re
import base64
import imageio.v2 as imageio
from streamlit_image_select import image_select
from skimage import exposure
# 读取tiff图片堆并变成数组的形式
def tifread(path):
    img = Image.open(path)
    images = []
    for i in range(img.n_frames):
        img.seek(i)
        images.append(np.array(img))
    return np.array(images)
# 读取三组tiff图片堆，将每一组相同次序图片进行拼接，以数组的形式输出
def joint_img(path1,path2,path3):
    img1 = Image.open(path1)
    img2 = Image.open(path2)
    img3 = Image.open(path3)
    images = []
    for i in range(img1.n_frames):
        img1.seek(i)
        img2.seek(i)
        img3.seek(i)
        img1_array = np.array(img1)
        img2_array = np.array(img2)
        img3_array = np.array(img3)
        img1_array = exposure.rescale_intensity(img1_array, in_range=(np.min(img1_array), np.max(img1_array)), out_range='uint16')
        img2_array = exposure.rescale_intensity(img2_array, in_range=(np.min(img2_array), np.max(img2_array)), out_range='uint16')
        img3_array = exposure.rescale_intensity(img3_array, in_range=(np.min(img3_array), np.max(img3_array)), out_range='uint16')
        new_array = np.concatenate([img1_array,img2_array,img3_array],axis=1)
        # new_image = Image.new("I;16",(img1.size[0]*3,img1.size[1]))
        # loc1,loc2,loc3 = (0,0),(img1.size[0],0),(img1.size[0]*2,0)
        # new_image.paste(img1,loc1)
        # new_image.paste(img2,loc2)
        # new_image.paste(img3,loc3)
        # print(new_image)
        # images.append(np.array(new_image))
        images.append(new_array)
    return np.array(images)
# 接收数组形式存储的图片数据并转换为gif动图
def gif_create(data):
    tif_list = []
    for i in range(0, data.shape[0] - 1):
        cv2.imwrite("storage.tif", data[i])
        img = cv2.imread("storage.tif")
        tif_list.append(img)
    imageio.mimsave("my_data.gif",tif_list,'GIF',duration=200,loop=0)
    # return "my_data.gif"
# 接收数组形式存储的图片数据并转换为mp4格式视频
def video_create(data,name):
    fourcc = cv2.VideoWriter_fourcc('X','2','6','4')
    videowrite = cv2.VideoWriter(f"{name}.mp4",fourcc,10,(data.shape[2],data.shape[1]))
    for i in range(0, data.shape[0] - 1):
        cv2.imwrite("storage.tif", data[i])
        img = cv2.imread("storage.tif")
        videowrite.write(img)
    videowrite.release()
    video_path = f"{name}.mp4"
    return video_path
# 接收gif动图路径并输出在页面上(image_select方法)
def gif_show(gif_path):
    index = image_select(label="input",
                 images=[gif_path],
                 use_container_width=False, return_value="index")
    return index
# 接收gif动图路径并输出在页面上(markdown方法)
def download_gif(gif_path,col,name):
    with open(gif_path,'rb') as f:
      contents = f.read()
      data_url = base64.b64encode(contents).decode("utf-8")
      col.write(name)
      col.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="gif" width=100% height=100%>',
    unsafe_allow_html=True,)
      # st.write('\n')
      # st.download_button('Download GIF', f, file_name=filename)
# 读取svg文件
def read_svg(path_svg):
    try:
        with open(path_svg, "r") as file:
            svg_logo = file.read().splitlines()
            _maped_list = map(str, svg_logo)
            svg_logo = "".join(_maped_list)
            temp_svg_logo = re.findall("<svg.*</svg>", svg_logo, flags=re.IGNORECASE)
            svg_logo = temp_svg_logo[0]
    except:  # None
        svg_logo = '<svg xmlns="http://www.w3.org/2000/svg" width="150px" height="1px" viewBox="0 0 150 1"></svg>'
    return svg_logo
# 将svg图片显示在页面上
def render_svg(svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = (
        r"""
        <div align="center">
        <img src="data:image/svg+xml;base64,%s" alt="SVG Image" style="width:18em; float:left;"/>
        </div>
        """
        % b64
    )
    return html
    # st.markdown(html, unsafe_allow_html=True)
def page_one():
    # 显示网页名称
    st.set_page_config(layout="wide", page_title="Deep Wonder")
    # 网页LOGO与标题
    with st.container():
        col1, col2, col3, col4 = st.columns([1,2,1,5.5])
        LOGO = Image.open("LOGO-new.png")
        st.markdown("""
        <style>
            .center{
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
        """,unsafe_allow_html=True)
        col2.image(LOGO, use_column_width=True)
        # col2.markdown(f"<div class='center'><img src='{LOGO}'></div>",unsafe_allow_html=True)
        col2.markdown("<h2 style='text-align: center;'>DeepDefinite</h2>",unsafe_allow_html=True)
        col4.markdown("<h2 style='text-align: center;'>Introduction</h2>",unsafe_allow_html=True)
        col4.markdown("<p style='font-size: 20em;'>DeepDefinite, a Deep Learning-based Widefield Neuron Finder with Self-supervi-<br>sion, is a pioneering tool for eliminating fluctuating background in one-photon<br>calcium imaging via self-supervised learning. This website offers the facility to<br>upload your captured one-photon images for swift online processing or to peruse<br>our preloaded demo datasets. Furthermore, DeepDefinite can be conveniently<br>downloaded as a Fiji plugin, thereby circumventing the need for a Python environ-<br>ment, or the complete software can be operated directly from our GitHub reposito-<br>ry: https://github.com/songxf1011/SSFA.</p>",unsafe_allow_html=True)
    st.markdown("\n")
    st.markdown("\n")
    # 网页视频与上传文件
    with st.container():
        col5, col6 = st.columns([1,1])
        # col5.markdown("<h2 style='text-align: center;'>Our Video</h2>",unsafe_allow_html=True)
        col5.video("https://www.youtube.com/watch?v=OMkEVX23BdM")
        # col6.markdown("<h2 style='text-align: center;'>Upload Data</h2>",unsafe_allow_html=True)
        st.session_state.my_upload = col6.file_uploader("Upload a file only tiff",type=["tiff"])
        if st.session_state.my_upload is not None:
            data = tifread(st.session_state.my_upload)
            gif_create(data)
            my_data = Image.open("my_data.gif")
            with col6:
                col6.markdown("<h5 style='font-weight:bolder;'>Describe your data such that we pair the best model for you!</h5>",unsafe_allow_html=True)
                col6_parameter,col6_data = st.columns([2,1])
                pixel_size = col6_parameter.text_input("Pixel size:")
                neuron_diameter = col6_parameter.text_input("Neuron diameter in pixel:")
                frame_rate = col6_parameter.text_input("Frame rate:")
                col6_data.image(my_data,use_column_width=True)
                if col6_data.button("Submit yes?"):
                    st.session_state.page = "two"
                    st.experimental_rerun()
    # 显示不同选项并产生对应数据
    with st.container():
        st.markdown("\n")
        col_option,col_example = st.columns([4,3])
        with col_option:
            st.markdown("<h4>Options</h4>",unsafe_allow_html=True)
            # col_option.markdown("<h5 style='font-weight:bolder;'>Devices</h5>",unsafe_allow_html=True)
            devices = image_select(label="Devices",images=["miniscope v3.png","miniscope v4.png","Widefield.png","Macroscope.png"],captions=["Miniscope v3","Miniscope v4","Widefield microscope","Macroscope"],use_container_width=False,return_value="index")
            # col_option.markdown("<h5 style='font-weight:bolder;'>Animals</h5>", unsafe_allow_html=True)
            animals = image_select(label="Animals",images=["mouse.png","zebrafish.png","drosophila.png"],captions=["Mouse","Zebrafish","Drosophila"],use_container_width=False,return_value="index")
            # col_option.markdown("<h5 style='font-weight:bolder;'>Categories</h5>", unsafe_allow_html=True)
            types = image_select(label="Type",images=["aav transduce.png","transgenetic.png"],captions=["AAV transduce","Transgenetic"],use_container_width=False,return_value="index")
        with col_example:
            if devices == 0:
                devices_text = "Miniscope v3"
            elif devices == 1:
                devices_text = "Miniscope v4"
            elif devices == 2:
                devices_text = "Widefield microscope"
            else:
                devices_text = "Macroscope"
            if animals == 0:
                animals_text = "Mouse"
            elif animals == 1:
                animals_text = "Zebrafish"
            else:
                animals_text = "Drosophila"
            if types == 0:
                types_text = "AAV transduce"
            else:
                types_text = "Transgenetic"
            if 'index_current' not in st.session_state:
                st.session_state.index_current = 0
            if devices==0 and animals==0 and types==0:
                st.markdown(
                    f"<h4 style='text-align: center;'>Dataset info</h4><h5>Device:&nbsp&nbsp{devices_text}</h5><h5>Animal:&nbsp&nbsp{animals_text}</h5><h5>Type:&nbsp&nbsp{types_text}</h5><h5>Acqusition:&nbsp&nbsp</h5><h5>No:&nbsp&nbsp{st.session_state.index_current + 1}</h5>"
                    , unsafe_allow_html=True)
                st.session_state.index = image_select(label="",images=["input1.gif","input2.gif","input3.gif"],use_container_width=False,return_value="index")
                if st.session_state.index != st.session_state.index_current:
                    st.session_state.index_current = st.session_state.index
                    st.experimental_rerun()
                if st.button("Submit yes? "):
                    if st.session_state.my_upload is not None:
                        st.error("You have uploaded files, please don't use examples!")
                    else:
                        st.session_state.page = "two"
                        st.experimental_rerun()

        st.markdown("\n")
        st.markdown("\n")
        st.markdown("\n")
        st.markdown("##### Contact: xxxxxxxxxxxx, bioRxiv, 2023.")
def page_two():
    # 显示网页名称
    st.set_page_config(layout="wide", page_title="Deep Wonder")
    # 网页LOGO与标题
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 2, 1, 5.5])
        LOGO = Image.open("LOGO-new.png")
        col2.image(LOGO, use_column_width=True)
        # col2.markdown(f"<div class='center'><img src='{LOGO}'></div>",unsafe_allow_html=True)
        col2.markdown("<h2 style='text-align: center;'>DeepDefinite</h2>", unsafe_allow_html=True)
        col4.markdown("<h2 style='text-align: center;'>Introduction</h2>", unsafe_allow_html=True)
        col4.markdown(
            "<h5>DeepDefinite, a Deep Learning-based Widefield Neuron Finder with Self-supervi-<br>sion, is a pioneering tool for eliminating fluctuating background in one-photon<br>calcium imaging via self-supervised learning. This website offers the facility to<br>upload your captured one-photon images for swift online processing or to peruse<br>our preloaded demo datasets. Furthermore, DeepDefinite can be conveniently<br>downloaded as a Fiji plugin, thereby circumventing the need for a Python environ-<br>ment, or the complete software can be operated directly from our GitHub reposito-<br>ry: https://github.com/songxf1011/SSFA.</h5>",
            unsafe_allow_html=True)
    st.markdown("\n")
    st.markdown("\n")
    if st.button("Try another one"):
        st.session_state.page = "one"
        st.experimental_rerun()
    if st.session_state.my_upload is None:
        # st.markdown("## Process & Result")
        with st.container():
            col_video,col_occupied1 = st.columns([3,1])
            col_video.markdown("##### WD & DeepWonder & 2p(high NA)")
            # col_input, col_network_processed, col_2p_ground_truth = st.columns([1, 1, 1])
            col_video.video(open(f"video{st.session_state.index+1}.mp4","rb").read())
            # download_gif(f"input{index+1}.gif", col_input, "input")
            # download_gif(f"network_processed{index+1}.gif",col_network_processed,"network_processed")
            # download_gif(f"2p_ground_truth{index+1}.gif",col_2p_ground_truth,"2p_ground_truth")
        with st.container():
            image_seg = Image.open(f"patch_seg{st.session_state.index+1}.tiff")
            image_sig = render_svg(read_svg(f"patch_sig{st.session_state.index+1}.svg"))
            col_seg, col_sig, col_occupied2 = st.columns([1, 1, 2])
            col_seg.markdown("##### Segmentation Spatial Mask")
            col_seg.image(image_seg, use_column_width=True)
            col_sig.markdown("##### Segmentation Temporal Mask")
            col_sig.markdown(image_sig, unsafe_allow_html=True)
    else:
        data = tifread(st.session_state.my_upload)
        # gif_path = gif_create(data)
        # gif_create(data)
        video_create(data, "my_data")
        col_my_data1, col_my_data2 = st.columns([1, 1])
        col_my_data1.video(open("my_data.mp4", "rb").read())
        # index = gif_show(gif_path)
        # download_gif(gif_path,st, "input")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("##### If you like the results, go to the documentation or github to learn how to install DeepDefinite.")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("##### Contact: xxxxxxxxxxxx, bioRxiv, 2023.")

if 'page' not in st.session_state:
    st.session_state.page = "one"
if st.session_state.page == "one":
    page_one()
else:
    page_two()
