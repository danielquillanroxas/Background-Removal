import streamlit as st


# set layout
import base64
import requests
st.set_page_config(layout='wide')
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates as im_coordinates
import cv2
import numpy as np

api_endpoint = 'https://danielquillanroxas.us-east-1.modelbit.com/v1/remove_background/latest'
# from streamlit_dimensions import st_dimensions

col01, col02 = st.columns(2)

# file uploader
file = col02.file_uploader('', type=['jpeg', 'png', 'jpg'])

# read image
if file is not None:
    image = Image.open(file).convert('RGB')

    image = image.resize((540, int(image.height * 560 / image.width)))



    # create buttons
    col1, col2 = col02.columns(2)

    placeholder0 = col02.empty()
    with placeholder0:
        value = im_coordinates(image)
        if value is not None:
            print(value)


    if col1.button('Original', use_container_width=True):
        placeholder0.empty()
        placeholder1 = col02.empty()
        with placeholder1:
            col02.image(image, use_column_width=True)

    if col2.button('Remove background', type='primary', use_container_width = True ):
        placeholder0.empty()
        placeholder2 = col02.empty()

        _, image_bytes = cv2.imencode('.png', np.asarray(image))

        image_bytes = image_bytes.tobytes()

        image_bytes_encoded_base64 = base64.b64encode(image_bytes).decode('utf-8')

        api_data = {"data": [image_bytes_encoded_base64, value['x'], value['y']]}
        response = requests.post(api_endpoint, json=api_data)

        result_image = response.json()['data']

        result_image_bytes = base64.b64decode(result_image)

        result_image = cv2.imdecode(np.frombuffer(result_image_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        with placeholder2:
            col02.image(result_image, use_column_width=True)

    # visualize image
    # click on image, get coordinates



    # call api