import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
    ##initialize our streamlit app

st.set_page_config(page_title="AI Tourist Advisor 🚀")

st.header("AI Tourist Advisor ✈️")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total about this palace")

input_prompt="""
You are an expert in Tourism and know the history of palaces where you need to see the Tourist palaces from the image
               and tell them the detail histroy of that palace, also provide the details of every palace like this format

               1. Date 1 - history of that palace
               2. Date 2 - history of that palace
               3. Date 3 - history of that palace
               ----
               ----
            Finally you can also mention the  if this palace is a tourist hotspot or not and also recommend some  tourist palace nearby with 
            brief summary about that

            1. Recommend Palace 1 - Summary of that place
            2. Recommend Palace 2 - Summary of that place
            ------
            ------


"""
## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)

