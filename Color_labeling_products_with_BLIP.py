import openai
import streamlit as st
from streamlit_chat import message
from PIL import Image
import os 
import pandas as pd
from io import StringIO, BytesIO
import requests
###
from st_pages import show_pages_from_config, add_page_title
# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()
show_pages_from_config()
###
from lavis.models import load_model_and_preprocess
import torch
#

model, vis_processors, txt_processors = load_model_and_preprocess(name="blip_vqa", model_type="vqav2", is_eval=True, device=device)
# ask a random question.
question = "Which city is this photo taken?"
image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
question = txt_processors["eval"](question)
model.predict_answers(samples={"image": image, "text_input": question}, inference_method="generate")
# ['singapore']


show_pages_from_config()

def load_sample_image(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # load sample image
    raw_image = Image.open("docs/_static/merlion.png").convert("RGB")
    return device, raw_image

# setup device to use
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# load sample image
raw_image = Image.open("docs/_static/merlion.png").convert("RGB")

def generate_response( productpage_input, productmainimage_input):

    with open('./assets/prompt1.txt', 'r') as file:
        # prompt_og_txt = file.read()
        # prompt_txt = prompt_og_txt
        # prompt_txt = prompt_txt.replace('<<<productpage>>>', productpage_input)
        # prompt_txt = prompt_txt.replace('<<<productmainimage>>>', productmainimage_input)


        prompt_txt = productpage_input

        print(prompt_txt)

        model, vis_processors, txt_processors = load_model_and_preprocess(name="blip_vqa", model_type="vqav2", is_eval=True, device=device)
        # ask a random question.
        question = "Which city is this photo taken?"
        image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
        question = txt_processors["eval"](question)
        model.predict_answers(samples={"image": image, "text_input": question}, inference_method="generate")
        # ['singapore']
        message=completion.choices[0].text
        return message

#######
aldo_logo = Image.open('./assets/aldo_logo.png')
st.image(aldo_logo, width = 100)


#storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []


productpage_input=st.text_input("Product page url:",key='productpage_input'
 ,value="https://www.aldoshoes.com/ca/en/women/jermeyyx-black/p/13559413")
st.write("Example: https://www.aldoshoes.com/ca/en/women/jermeyyx-black/p/13559413")
st.markdown("""---""")

productmainimage_input=st.text_input("Product main image url:",key='productmainimage_input'
 ,value="https://media.aldoshoes.com/v3/product/jermeyyx/007-002-043/jermeyyx_black_007-002-043_main_sq_gy_1000x1000.jpg")
st.write("Example: https://media.aldoshoes.com/v3/product/jermeyyx/007-002-043/jermeyyx_black_007-002-043_main_sq_gy_1000x1000.jpg")
st.markdown("""---""")

if productpage_input and productmainimage_input:
    output=generate_response( productpage_input, productmainimage_input)

    # Get the csv part
    delim = 'Final output as csv:'
    csv_string_part = output.partition(delim)[2]

    print("csv_string_part is : \n")

    print(csv_string_part)


    # Convert String into StringIO
    csvStringIO = StringIO(csv_string_part)

    # Then into df
    df = pd.read_csv(csvStringIO, sep=",", header=0)

    df.columns.values[0] = "Color_from_GPT"
    df.columns.values[1] = "Color_from_GPT_main"
    df.columns.values[2] = "Color_from_GPT_alt1"
    df.columns.values[3] = "Color_from_GPT_alt2"
    df.columns.values[4] = "Color_from_GPT_alt3"
    df.columns.values[5] = "Style"
    df.columns.values[6] = "Official_color"
    
    Color_from_GPT = df['Color_from_GPT'][0].strip()
    Official_color = df['Official_color'][0].strip()

    if Color_from_GPT == Official_color:
        df['Alert'] = 'No - GPT agrees'
    if Color_from_GPT != Official_color:
        df['Alert'] = 'Yes - GPT disagrees'

    df = df[['Alert', 'Style', 'Official_color', 'Color_from_GPT', 
             'Color_from_GPT_main', 'Color_from_GPT_alt1', 'Color_from_GPT_alt2',
               'Color_from_GPT_alt3']]

    # Display an interactive table
    st.dataframe(df)

    # Display Main image
    response = requests.get(productmainimage_input)
    productmainimage_image = Image.open(BytesIO(response.content))
    st.image(productmainimage_image, width = 400, caption = df['Style'][0] )



    #store the output
    st.session_state['past'].append(productpage_input)
    st.session_state['generated'].append(output)
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


