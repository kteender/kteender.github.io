import subprocess
import os
#YOU NEED TO INSTALL FFMPEG
def fix_file_sizes(dir):
    print('test')
    fix_list = [item for item in os.listdir(dir) if os.path.getsize(os.path.join(dir,item)) >= 3000000]
    to_mp4_types = ['gif', 'GIF', 'mov', 'MOV', 'mp4', 'MP4']
    new_dir = os.path.join(dir, 'converted_files')
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    for file in fix_list:
        if file.split('.')[-1] in to_mp4_types:
            name = file.split('.')[-2]+'.webm'
            new_file = os.path.join(new_dir,name)
            #cmd = 'ffmpeg -i %s -vcodec libx264 -crf 18 %s' % (os.path.join(dir, file), new_file)
            cmd = 'ffmpeg -i %s -pix_fmt yuv420p %s' % (os.path.join(dir, file), new_file)
            #cmd = 'ffmpeg -i frame_%05d.jpg -vcodec libx264 \ -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -r 24 \ -y -an video.mp4' 
            print(cmd)
            subprocess.call(cmd)

def convert_png_to_jpg(dir):
    new_dir = os.path.join(dir, 'converted_files')
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    fix_list = [item for item in os.listdir(dir) if item.split(".")[-1].lower() == 'png']
    for file in fix_list:
        name = file.split('.')[0]
        old_file = os.path.join(dir, file)
        new_file = os.path.join(new_dir, name+'_converted.jpeg')
        cmd = """ffmpeg -i %s -vf "scale='min(1000,iw)':min'(1000,ih)':force_original_aspect_ratio=decrease" -q:v 1 -dpi 72 %s""" % (old_file, new_file)
        #cmd.replace('input.png', old_file)
        #cmd.replace('output.jpg', new_file)
        #cmd = 'ffmpeg -i %s %s' % (old_file, new_file)
        print(cmd)
        subprocess.call(cmd)

d = 'D://kteender.github.io//img//drawings//'
convert_png_to_jpg(d)

#fix_file_sizes('D:\\kteender.github.io\\img\\01')
#fix_file_sizes('D:\\kteender.github.io\\img\\2023-07-16-outlines')