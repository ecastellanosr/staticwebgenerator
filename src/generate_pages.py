from markdown_to_block import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType
import os


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            counter = 0
            for letter in block[:6]:
                if letter == "#":
                    counter += 1
            if counter == 1:
                return block[1:].lstrip()
    raise Exception("Could not extract title as there in no h1 header in markdown")

def generate_page(from_path, template_path,dest_path,basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    try:
        with open(from_path, "r") as f:
            markdown_string = f.read()  
    except Exception as e:
        return f"Error: {e}"
     
    try:
        with open(template_path, "r") as f:
            template_string = f.read() 
    except Exception as e:
        return f"Error: {e}"
    
    title = extract_title(markdown_string)

    template_string = template_string.replace('<title>{{ Title }}</title>',f"<title> {title} </title>")
    markdown_node = markdown_to_html_node(markdown_string)
    html = markdown_node.to_html()
    template_string = template_string.replace('<article>{{ Content }}</article>',f"<article>{ html }</article>")
    template_string = template_string.replace('href="/',f'href="{basepath}')
    template_string = template_string.replace('src="/',f'src="{basepath}')
    
    try:
        with open(dest_path, "w") as f:
            f.write(template_string)  
    except Exception as e:
        return f"Error: {e}"

  
def generate_pages_recursive(dir_from_path, template_path, dir_dest_path,basepath):
    #it copies the directory objects and recursively pastes it to the same directory but in the new destination
    if not os.path.exists(dir_dest_path):
        os.mkdir(dir_dest_path)

    old_directory_files =  os.listdir(dir_from_path)
    if old_directory_files:
        print("there are files in static directory")
        for file in old_directory_files:
            filepath = os.path.join(dir_from_path,file)
            if os.path.isdir(filepath):
                destination = os.path.join(dir_dest_path,file)
                generate_pages_recursive(filepath,template_path,destination)
            elif os.path.isfile(filepath) and file.endswith(".md"):
                filename = file.split(".",1)[0]
                destination = os.path.join(dir_dest_path,filename + ".html")
                generate_page(filepath,template_path,destination,basepath)
        return