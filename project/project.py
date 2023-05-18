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

def gif_create(data,name):
    tif_list = []
    for i in range(0, data.shape[0] - 1):
        cv2.imwrite("storage.tif", data[i])
        img = cv2.imread("storage.tif")
        tif_list.append(img)
    imageio.mimsave(f'{name}.gif',tif_list,'GIF',fps=5,loop=0)
    # gif = Image.open(f"{name}.gif")
    gif_path = f'{name}.gif'
    return gif_path

def download_gif(gif_path,col,name):
    with open(gif_path,'rb') as f:
      contents = f.read()
      data_url = base64.b64encode(contents).decode("utf-8")
      col.write(name)
      col.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="gif" width=100% height=100%>',
    unsafe_allow_html=True,)
      # st.write('\n')
      # st.download_button('Download GIF', f, file_name=filename)


# def video_create(data,name):
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     videowrite = cv2.VideoWriter(f"{name}.mp4",fourcc,10,(data.shape[2],data.shape[1]))
#     for i in range(0, data.shape[0] - 1):
#         cv2.imwrite("storage.tif", data[i])
#         img = cv2.imread("storage.tif")
#         videowrite.write(img)
#     video_path = f"{name}.mp4"
#     return video_path

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


# st.sidebar.write("## Upload and download :gear:")
# st.write("## Hello")
st.set_page_config(layout="wide", page_title="Deep Wonder")
# st.write("## Remove background from your image")
# st.write(
    # ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](https://github.com/tyler-simons/BackgroundRemoval) on GitHub. Special thanks to the [rembg library](https://github.com/danielgatis/rembg) :grin:"
# )
# st.sidebar.write("## Upload and download :gear:")

# Download the fixed image
# def convert_image(img):
#     buf = BytesIO()
#     img.save(buf, format="PNG")
#     byte_im = buf.getvalue()
#     return byte_im
with st.container():
    col1, col2, col3, col4 = st.columns([1,2.5,0.65,5.35])
#     LOGO = Image.open("images/LOGO-new.png")
#     GitHub = Image.open("./images/GitHub.png")
#     arxiv = Image.open("./images/arxiv.png")
#     col1.image(LOGO,width=120)
    col2.title("Deep Wonder")
    # col3.image(GitHub,width=75)
    # col4.image(arxiv,width=100)
st.markdown("\n")
st.markdown("\n")
if page == 1:
    with st.container():
        col5, col6 = st.columns([1,1])
        col5.video("https://www.youtube.com/watch?v=OMkEVX23BdM")
        col6.header("Upload Data")
        # col6.markdown("\n")
        my_upload = col6.file_uploader("Upload a file only tiff",type=["tiff"])

    # with st.container():
    #     if my_upload is None:
    #         st.markdown("\n")
    #         st.markdown("### Three examples(input) are as follows:")
    #         template1 = tif.imread("./web_demo/macroscope/patch_wd.tiff")
    #         template2 = tif.imread("./web_demo/miniscope_v4/patch_wd.tiff")
    #         template3 = tif.imread("./web_demo/widefield_highNA/patch_wd.tiff")
    #         max_slices1 = template1.shape[0]
    #         max_slices2 = template2.shape[0]
    #         max_slices3 = template3.shape[0]

    #         col7, col8, col9 = st.columns([1, 1, 1])
    #         slice_index1 = col7.slider("Example1_Slice", min_value=1, max_value=max_slices1, value=1, step=1)
    #         fig1, ax1 = plt.subplots()
    #         ax1.imshow(template1[slice_index1 - 1], cmap="gray", aspect='equal')
    #         ax1.set_title(f"Slice {slice_index1}")
    #         ax1.axis("off")
    #         plt.tight_layout()
    #         col7.pyplot(fig1)
    #         plt.close(fig1)

    #         slice_index2 = col8.slider("Example2_Slice", min_value=1, max_value=max_slices2, value=1, step=1)
    #         fig2, ax2 = plt.subplots()
    #         ax2.imshow(template2[slice_index2 - 1], cmap="gray", aspect='equal')
    #         ax2.set_title(f"Slice {slice_index2}")
    #         ax2.axis("off")
    #         plt.tight_layout()
    #         col8.pyplot(fig2)
    #         plt.close(fig2)

    #         slice_index3 = col9.slider("Example3_Slice", min_value=1, max_value=max_slices3, value=1, step=1)
    #         fig3, ax3 = plt.subplots()
    #         ax3.imshow(template3[slice_index3 - 1], cmap="gray", aspect='equal')
    #         ax3.set_title(f"Slice {slice_index3}")
    #         ax3.axis("off")
    #         plt.tight_layout()
    #         col9.pyplot(fig3)
    #         plt.close(fig3)
    #     else:
    #         st.markdown("\n")
    #         st.markdown("### The real input is as follows:")
    #         template = tif.imread(my_upload)
    #         max_slices = template.shape[0]
    #         col7, col8, col9 = st.columns([1, 1, 1])
    #         slice_index = col7.slider("Slice", min_value=1, max_value=max_slices, value=1, step=1)
    #         fig, ax = plt.subplots()
    #         ax.imshow(template[slice_index-1], cmap="gray", aspect='equal')
    #         ax.set_title(f"Slice {slice_index}")
    #         ax.axis("off")
    #         # plt.tight_layout()
    #         col7.pyplot(fig)
    #         plt.close(fig)
    with st.container():
        st.markdown("\n")
        st.write("## Options")
        devices = image_select(label="Choose in four devices:",images=["./images/miniscope v3.png","./images/miniscope v4.png","./images/Widefield.png","./images/Macroscope.png"],captions=["Miniscope v3","Miniscope v4","Widefield microscope","Macroscope"],use_container_width=False,return_value="index")
        animals = image_select(label="Choose in three animals:",images=["./images/mouse.png","./images/zebrafish.png","./images/drosophila.png"],captions=["Mouse","Zebrafish","Drosophila"],use_container_width=False,return_value="index")
        categories = image_select(label="Choose in two categories:",images=["./images/aav transduce.png","./images/transgenetic.png"],captions=["AAV transduce","Transgenetic"],use_container_width=False,return_value="index")
        # st.write(devices)
        # st.write(animals)
        # st.write(categories)
        if my_upload is None:
            st.write("## Examples")
            if devices==0 and animals==0 and categories==0:
                index = image_select(label="input",images=["./web_demo/1/input.gif","./web_demo/2/input.gif","./web_demo/3/input.gif"],use_container_width=False,return_value="index")
                # st.write(index)
                st.markdown("## Process & Result")
                with st.container():
                    col_input, col_network_processed, col_2p_ground_truth = st.columns([1, 1, 1])
                    download_gif(f"./web_demo/{index+1}/input.gif", col_input, "input")
                    download_gif(f"./web_demo/{index+1}/network_processed.gif",col_network_processed,"network_processed")
                    download_gif(f"./web_demo/{index+1}/2p_ground_truth.gif",col_2p_ground_truth,"2p_ground_truth")
                with st.container():
                    image_seg = Image.open(f"./web_demo/{index+1}/patch_seg.tiff")
                    image_sig = render_svg(read_svg(f"./web_demo/{index+1}/patch_sig.svg"))
                    # image_sig = cv2.imread("./web_demo/macroscope/patch_sig.svg")
                    col_seg, col_sig = st.columns([1, 1])
                    col_seg.write("Segmentation Spatial Mask")
                    col_seg.image(image_seg, width=600)
                    col_sig.write("Segmentation Temporal Mask")
                    col_sig.markdown(image_sig, unsafe_allow_html=True)
        else:
            st.write("## Your Data")
            data = tifread(my_upload)
            gif_path = gif_create(data,"my_data")
            index = image_select(label="input",
                                 images=["my_data.gif"],
                                 use_container_width=False, return_value="index")
            download_gif(f"my_data.gif",st, "input")

        # devices = Image.open("./images/devices.png")
        # animals = Image.open("./images/animals.png")
        # categories = Image.open("./images/categories.png")
        # col_choice1, col_choice2, col_choice3 = st.columns([1,1,1])
        # col_choice1.write(devices)
        # col_choice1.selectbox('Choose in four devices:',["Miniscope v3","Miniscope v4","Widefield microscope","Macroscope"])
        # col_choice1.image(devices)
        # col_choice2.selectbox('Choose in three animals:',["Mouse","Zebrafish","Drosophila"])
        # col_choice2.image(animals)
        # col_choice3.selectbox('Choose in two categories:',["AAV transduce","Transgenetic"])
        # col_choice3.image(categories)

        # with st.container():
            # template_input = tifread("./web_demo/macroscope/patch_wd.tiff")
            # gif_path_input = gif_create(template_input,"input")
            # template_network_processed = tif.imread("./web_demo/macroscope/patch_rmbg.tiff")
            # gif_path_network_processed = gif_create(template_network_processed,"network_processed")
            # template_2p_ground_truth = tif.imread("./web_demo/macroscope/patch_2p.tiff")
            # gif_path_2p_ground_truth = gif_create(template_2p_ground_truth,"2p_ground_truth")

            # max_slices = template_input.shape[0]
            # slice_index = st.slider("Change Slice", min_value=1, max_value=max_slices, value=1, step=1)
            # col_input, col_network_processed, col_2p_ground_truth = st.columns([1, 1, 1])
            # download_gif(gif_path_input,col_input,"input")
            # download_gif(gif_path_network_processed, col_network_processed, "network_processed")
            # download_gif(gif_path_2p_ground_truth, col_2p_ground_truth, "2p_ground_truth")
            # download_gif("input.gif", col_input, "input")
            # download_gif("network_processed.gif",col_network_processed,"network_processed")
            # download_gif("2p_ground_truth.gif",col_2p_ground_truth,"2p_ground_truth")

            # col_input.video(open("./input.mp4","rb").read(),start_time=0)
            # col_network_processed.video(open(video_path_network_processed, "rb").read(), start_time=0)
            # col_2p_ground_truth.video(open(video_path_2p_ground_truth, "rb").read(), start_time=0)
            # fig1, ax1 = plt.subplots()
            # ax1.imshow(template_input[slice_index - 1], cmap="gray", aspect='equal')
            # ax1.set_title(f"Input: Slice {slice_index}")
            # ax1.axis("off")
            # # plt.tight_layout()
            # col_input.pyplot(fig1)
            # plt.close(fig1)
            # # slice_index = col_network_processed.slider("Network Processed", min_value=1, max_value=max_slices, value=1, step=1)
            # fig2, ax2 = plt.subplots()
            # ax2.imshow(template_network_processed[slice_index - 1], cmap="gray", aspect='equal')
            # ax2.set_title(f"Network Processed: Slice {slice_index}")
            # ax2.axis("off")
            # # plt.tight_layout()
            # col_network_processed.pyplot(fig2)
            # plt.close(fig2)
            # # slice_index = col_2p_ground_truth.slider("2p Ground Truth", min_value=1, max_value=max_slices, value=1, step=1)
            # fig3, ax3 = plt.subplots()
            # ax3.imshow(template_2p_ground_truth[slice_index - 1], cmap="gray", aspect='equal')
            # ax3.set_title(f"2p Ground Truth: Slice {slice_index}")
            # ax3.axis("off")
            # # plt.tight_layout()
            # col_2p_ground_truth.pyplot(fig3)
            # plt.close(fig3)

            # fig, ax = plt.subplots()
            # ax.imshow(image_seg, cmap="gray", aspect='equal')
            # ax.set_title(f"Segmentation Spatial Mask")
            # ax.axis("off")
            # # plt.tight_layout()
            # col_seg.pyplot(fig)
            # plt.close(fig)

            # fig2, ax2 = plt.subplots()
            # ax2.imshow(image_sig, cmap="gray", aspect='equal')
            # ax2.set_title(f"Segmentation Temporal Mask")
            # ax2.axis("off")
            # # plt.tight_layout()
            # col_sig.pyplot(fig)
            # plt.close(fig)
