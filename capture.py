import streamlit as st
from storage import supabase
from PIL import Image
import os
import tempfile


#UPLOADING IMAGE
def upload_image(image, name, ind = 0):
    
    #name
    #folder_path = "kelmith/"
    
    #image
    #image = Image.open("./arnold.jpg")

    with tempfile.NamedTemporaryFile(suffix=".jpg",delete=False) as temp:
        image.save(temp, format = "JPEG")
        temp_path = temp.name

    full_path = name + "/" + f"{name}_{ind}.jpg"

#uploading file
    res = supabase.storage.from_("images").upload(file=temp_path,path=full_path, file_options={"content-type": "image/jpeg"})
    print(f"res: {res}")


st.set_page_config(
    page_title="Scan Faces",
    page_icon="🎄"
)

st.header("Recording Faces")
st.info("Please enter the name of the person you want to record")

name = st.text_input("Name: ")

if name:
 
    
    st.warning("Please snap more than 3 pictures of yourself with variations of lighting and angles")
    st.divider()
    
    #initializing session to store images
    if "images" not in st.session_state:
        st.session_state.images = []
    
    #initilize counter to keep track of number of images
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    
    #initilize flag to keep track of when to stop recording
    if "flag" not in st.session_state:
        st.session_state.flag = False
        
    def stop_recording():
        st.session_state.flag = True
    
    while( not st.session_state.flag):
        image = st.camera_input("Click",key=f"image_{st.session_state.counter}")
        
        if image is not None:
            pic = Image.open(image)
            st.session_state.images.append(pic)
            st.session_state.counter += 1
            st.info(f"Images Captured: {st.session_state.counter}")
        st.button("Stop Recording",on_click=stop_recording,key=f"btn{st.session_state.counter}")
    
    st.success(f"you have captured {st.session_state.counter} images")
    gallery = st.session_state.images
    
    #UPLOADING TO SUPABASE
    if len(gallery) > 0:
        for ind in range(len(gallery)):
            upload_image(gallery[ind],name,ind)
    
    
    # LOCAL STORAGE
    
    # if len(gallery) > 0:
    #     dataset = "./images/known/"
    #     new_path = os.path.join(dataset,name)
    
    #     #to save current path and reuse
    #     current_path = os.getcwd()
        
    #     #FIXME:
    #     os.makedirs(new_path,exist_ok=True)
        
    #     #navigate to the new path
    #     os.chdir(new_path)
    #         #populate the new directory with images
    #     for ind in range(len(gallery)):
    #         gallery[ind].save(fp=f'{name}_{ind}.jpg',format='JPEG')
        
    #     #To take you back to load.
    #     os.chdir(current_path)