import os

file = 'D:\\kteender.github.io\\_posts\\technical-blog\\2019-08-11-animating-using-flat-planes-in-maya.md'
image_dir = 'D:\\kteender.github.io\\img\\2019-08-11-flat-planes\\'
img = image_dir.split('kteender.github.io')[-1]
print("image dir")
print(image_dir)
converted_dir = os.path.join(image_dir, 'converted_files')
print("converted dir")
print(converted_dir)
print('img')
print(img)

def fix_image_names():
    f1 = open(file, 'r', encoding="utf8")
    lines = f1.read().split('\n')
    new_lines = []
    f1.close()

    lower_imgs = [f.lower() for f in os.listdir(image_dir)]

    for i in range(0, len(lines)):
        line = lines[i]
        new_line = line
        #if "https://ktcgart.files.wordpress.com" in line:
        if "img src=" in line:
            first, last = line.split("img src=")
            spaces = last.split(" ")
            current_img = spaces[0]
            rest = (" ").join(spaces[1:])

            use_img = current_img
            current_file_name = use_img.split("/")[-1].replace("'", "").replace("\"", "")
            use_file_name = current_file_name
            if current_file_name not in os.listdir(image_dir):
                for i in range(0, len(lower_imgs)):
                    if current_file_name.lower() == lower_imgs[i]:
                        use_file_name = os.listdir(image_dir)[i]
                        break
                new_line = first+"img src='"+os.path.join('/img/2019-07-09-mobu-eye-rig/', use_file_name)+"' "+rest

        new_lines.append(new_line)

    save_str = "\n".join(new_lines)
    print("saving")
    new_file = 'D:\\kteender.github.io\\_posts\\technical-blog\\test.md'
    f2 = open(new_file, 'w', encoding="utf-8")
    f2.write(save_str)
    f2.close()

def png_jpg_compare():
    f1 = open(file, 'r', encoding="utf8")
    lines = f1.read().split('\n')
    new_lines = []
    f1.close()

    for i in range(0, len(lines)):
        line = lines[i]
        new_line = line
        #if "https://ktcgart.files.wordpress.com" in line:
        if "img src=" in line:
            if 'converted_files' not in line:
                print('line')
                print(line)
                first, last = line.split("img src=")
                spaces = last.split(" ")
                current_img = spaces[0]
                rest = (" ").join(spaces[1:])

                use_img = current_img
                current_file_name = use_img.split("/")[-1].replace("'", "").replace("\"", "")
                name_only = current_file_name.split('.')[0]
                current_file_path = os.path.join(image_dir, current_file_name)
                print("current_file_path")
                print(current_file_path)
                print("name only")
                print(name_only)
                converted_file_path = os.path.join(converted_dir, name_only+'_converted.jpeg')
                #converted_img = os.path.join(img, 'converted', name_only+'_converted.jpeg')
                converted_img = '\\'.join([img, 'converted_files', name_only+'_converted.jpeg'])
                print("converted_file_path")
                print(converted_file_path)

                if os.path.getsize(converted_file_path) < os.path.getsize(current_file_path):
                    print("it's smaller")
                    new_line = first+"img src='"+converted_img+"' "+rest
                    print("old line")
                    print(line)
                    print("new_line")
                    print(new_line)

        new_lines.append(new_line)

    save_str = "\n".join(new_lines)
    print("saving")
    new_file = 'D:\\kteender.github.io\\_posts\\technical-blog\\test.md'
    f2 = open(new_file, 'w', encoding="utf-8")
    f2.write(save_str)
    f2.close()

png_jpg_compare()



