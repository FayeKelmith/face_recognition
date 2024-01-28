import streamlit as st


st.set_page_config(
    page_title="Scan Faces",
    page_icon="📸 "
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
            st.session_state.images.append(image)
            st.session_state.counter += 1
            st.info(f"Images Captured: {st.session_state.counter}")
        st.button("Stop Recording",on_click=stop_recording,key=f"btn{st.session_state.counter}")
    
    st.success(f"you have captured {st.session_state.counter} images")
    