import os
from supload import upload_file

def upload_to_s3(input_folder,file_ext):
    osbj = os.listdir(input_folder)

    all_files = []
    for file in osbj:
        if file.endswith(file_ext):
            all_files.append(os.path.join(input_folder,file))
    return all_files




if __name__ == "__main__":
    all_files = upload_to_s3(r'C:\Users\Pankaj\Documents\GitHub\ziper','.zip')
    for file in all_files:
       upload_file(filename=file)
