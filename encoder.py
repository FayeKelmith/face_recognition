from storage import supabase
import os

known_faces = "./images/known/"

def download_images():
    # list all folders in the bucket
    folders  = supabase.storage.from_("images").list()

    for folder in folders:
        
        #Create local folder in known_faces/folder_name and if it exists, skip
        new_path = os.path.join(known_faces, folder["name"])
        if not os.path.exists(new_path):
            files = supabase.storage.from_("images").list(folder["name"])
            os.mkdir(known_faces + folder["name"]) #create folder
            # os.chdir(known_faces + folder["name"]) #change directory to new folder
            for file in files:
                #download file
                file_path = os.path.join(new_path,file["name"])
                with open(file_path,"wb+") as f:
                    data = supabase.storage.from_("images").download(f"{folder['name']}/{file['name']}")
                    f.write(data)
                    print(f"Downloading {file['name']}")
                    
                
                print("---------------------")
        else:
            continue
    print("Download Complete! 🎉 ")

        
#download_images()
