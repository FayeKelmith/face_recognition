from storage import supabase
from PIL import Image
import tempfile


bucket_name = "images"

def upload_image(image, name, ind = 0):
    
    #name
    #folder_path = "kelmith/"
    
    #image
    #image = Image.open("./arnold.jpg")

    with tempfile.NamedTemporaryFile(suffix=".jpg",delete=False) as temp:
        image.save(temp, format = "JPEG")
        temp_path = temp.name

    full_path = name + f"{name}_{ind}.jpg"

#uploading file
    res = supabase.storage.from_("images").upload(file=temp_path,path=full_path, file_options={"content-type": "image/jpeg"})
    print(f"res: {res}")

