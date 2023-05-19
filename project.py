import streamlit as st
import numpy as np
from PIL import Image
import cv2
import re
import base64
import imageio.v2 as imageio
from streamlit_image_select import image_select

def tifread(path):
    img = Image.open(path)
    images = []
    for i in range(img.n_frames):
        img.seek(i)
        images.append(np.array(img))
    return np.array(images)

def gif_create(data):
    tif_list = []
    for i in range(0, data.shape[0] - 1):
        cv2.imwrite("storage.tif", data[i])
        img = cv2.imread("storage.tif")
        tif_list.append(img)
    imageio.mimsave("my_data.gif",tif_list,'GIF',fps=5,loop=0)
    return "my_data.gif"

def download_gif(gif_path,col,name):
    with open(gif_path,'rb') as f:
      contents = f.read()
      data_url = base64.b64encode(contents).decode("utf-8")
      col.write(name)
      col.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="gif" width=100% height=100%>',
    unsafe_allow_html=True,)
      # st.write('\n')
      # st.download_button('Download GIF', f, file_name=filename)

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

def render_svg(svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = (
        r"""
        <div align="center">
        <img src="data:image/svg+xml;base64,%s" alt="SVG Image" style="width:35em;"/>
        </div>
        """
        % b64
    )
    return html
    # st.markdown(html, unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="Deep Wonder")
with st.container():
    col1, col2, col3, col4 = st.columns([1,2.5,0.65,5.35])
    LOGO = Image.open("LOGO-new.png")
    # GitHub = Image.open("GitHub.png")
    # arxiv = Image.open("arxiv.png")
    col1.image(LOGO,width=120)
    col2.title("Deep Wonder")
    # col3.image(GitHub,width=75)
    # col4.image(arxiv,width=100)
st.markdown("\n")
st.markdown("\n")
with st.container():
    col5, col6 = st.columns([1,1])
    col5.video("https://www.youtube.com/watch?v=OMkEVX23BdM")
    col6.header("Upload Data")
    my_upload = col6.file_uploader("Upload a file only tiff",type=["tiff"])

with st.container():
    st.markdown("\n")
    st.write("## Options")
    devices = image_select(label="Choose in four devices:",images=["miniscope v3.png","miniscope v4.png","Widefield.png","Macroscope.png"],captions=["Miniscope v3","Miniscope v4","Widefield microscope","Macroscope"],use_container_width=False,return_value="index")
    animals = image_select(label="Choose in three animals:",images=["mouse.png","zebrafish.png","drosophila.png"],captions=["Mouse","Zebrafish","Drosophila"],use_container_width=False,return_value="index")
    categories = image_select(label="Choose in two categories:",images=["aav transduce.png","transgenetic.png"],captions=["AAV transduce","Transgenetic"],use_container_width=False,return_value="index")
    if my_upload is None:
        st.write("## Examples")
        if devices==0 and animals==0 and categories==0:
            index = image_select(label="input",images=["input1.gif","input2.gif","input3.gif"],use_container_width=False,return_value="index")
            st.markdown("## Process & Result")
            with st.container():
                col_input, col_network_processed, col_2p_ground_truth = st.columns([1, 1, 1])
                download_gif(f"input{index+1}.gif", col_input, "input")
                download_gif(f"network_processed{index+1}.gif",col_network_processed,"network_processed")
                download_gif(f"2p_ground_truth{index+1}.gif",col_2p_ground_truth,"2p_ground_truth")
            with st.container():
                image_seg = Image.open(f"patch_seg{index+1}.tiff")
                image_sig = render_svg(read_svg(f"patch_sig{index+1}.svg"))
                col_seg, col_sig = st.columns([1, 1])
                col_seg.write("Segmentation Spatial Mask")
                col_seg.image(image_seg, width=600)
                col_sig.write("Segmentation Temporal Mask")
                col_sig.markdown(image_sig, unsafe_allow_html=True)
    else:
        st.write("## Your Data")
        data = tifread(my_upload)
        gif_path = gif_create(data)
#         index = image_select(label="input",
#                                  images=["my_data.gif"],
#                                  use_container_width=False, return_value="index")
        download_gif(gif_path,st,"input")
