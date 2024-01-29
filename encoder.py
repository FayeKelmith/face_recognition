from storage import supabase
import os
import face_recognition as fr
import numpy as np
import logging
import csv

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
    
def encode_image(img_path):
    picture = fr.load_image_file(img_path)
    face_location = fr.face_locations(picture)[0] 
    
    if face_location is None:
        logging.warning("No face found in image")
        return
    
    face_encodings = fr.face_encodings(picture) #encode face
    
    return face_encodings

def encode_photo_set(path):
    photos_list = os.listdir(path)
    if len(photos_list) == 0:
        logging.warning("No photos found in directory")
        return
    else:
        logging.info(f"Encoding photos...")
        
    features_list = []
    for photo in photos_list:
        photo_path = os.path.join(path,photo)
        features_list.append(encode_image(photo_path)) #append 
    
    
    features_mean = np.array(features_list, dtype=object).mean(axis=0) #calculate mean of face encodings   
    
    if features_mean is None:
        logging.warning("No face found in image | Terminating")
        return
    return features_mean 

def main():
    
    logging.basicConfig(level=logging.INFO) #set logging level to info
    
    logging.info("Downloading photos")
    download_images() #download images from supabase
    
    known_photos = os.listdir(known_faces)
    
    features = "./encodings/features.csv"
    with open(features,"w+") as f:  #create and open csv file
        writer = csv.writer(f)
        for album in known_photos:
            album_path = os.path.join(known_faces,album)
            album_encoding_mean = encode_photo_set(album_path)
            
            album_encoding_mean = np.insert(album_encoding_mean,0,album) #insert name at the beginning of the array 
            writer.writerow(album_encoding_mean)
        logging.info("Saved encodings to csv file")     
        

if __name__ == "__main__":
    main()