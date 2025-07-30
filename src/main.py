import os
import shutil
from generate_pages import generate_pages_recursive

def main():
    current_path =  os.path.dirname(__file__)
    static_web_generator_path = os.path.split(current_path)[0]
    public = os.path.join(static_web_generator_path,"public") 
    static = os.path.join(static_web_generator_path,"static")
    
    if os.path.exists(public):
        public_files =  os.listdir(public)
        if public_files:
            print("removing files")
            shutil.rmtree(public)
    if os.path.exists(static):
        copypaste_directories(static,public)
        
        content = os.path.join(static_web_generator_path,"content") 
        template = os.path.join(static_web_generator_path,"template.html") 
        generate_pages_recursive(content,template,public)
        
            

                
def copypaste_directories(old_directory,new_directory):
    #it copies the directory objects and recursively pastes it to the same directory but in the new destination
    os.mkdir(new_directory)
    old_directory_files =  os.listdir(old_directory)
    if old_directory_files:
        print("there are files in static directory")
        for file in old_directory_files:
            filepath = os.path.join(old_directory,file)
            if os.path.isdir(filepath):
                destination_directory = os.path.join(new_directory,file)
                copypaste_directories(filepath,destination_directory)
            else:
                shutil.copy(filepath,os.path.join(new_directory,file))
        return

if __name__ == "__main__":
    main()