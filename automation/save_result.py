import os
from handle_file import writeFile

file_path = 'perception/src/detection/test_yolo'
pwd=os.getcwd()

def saveResult(src_path = file_path, content_to_save = "Sample results content"):
    save_path = calcSavePath(src_path)
    if save_path:
        saveToPath(save_path, content_to_save)

def calcSavePath(path=file_path):
    try:
        x, _, y, z = path.split('/')
        z = z.split('.')[0]
        return f'results/{x}/{y}/{z}'
    except ValueError:
        print("Path format error, expected 'x/src/y/z'")
        return

def saveToPath(save_path, content_to_save, file_type = 'txt'):
    
    target_dir = os.path.join(pwd, save_path)
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, f"results.{file_type}")
    
    writeFile(target_file, content_to_save)
    print(f"File saved in: {target_dir}")
    
    
    