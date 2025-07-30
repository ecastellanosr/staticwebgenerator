import os
import shutil
import sys
from generate_pages import generate_pages_recursive


def main():
    basepath = sys.argv[1]
    if len(sys.argv) < 2:
       basepath = "/"
    
    current_path =  os.path.dirname(__file__)
    static_web_generator_path = os.path.split(current_path)[0]
    docs = os.path.join(static_web_generator_path,"docs") 
    static = os.path.join(static_web_generator_path,"static")
    
    if os.path.exists(docs):
        docs_files =  os.listdir(docs)
        if docs_files:
            print("removing files")
            shutil.rmtree(docs)
    if os.path.exists(static):
        copypaste_directories(static,docs)
        
        content = os.path.join(static_web_generator_path,"content") 
        template = os.path.join(static_web_generator_path,"template.html") 
        generate_pages_recursive(content,template,docs,basepath)
                
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