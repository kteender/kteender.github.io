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
            name = file.split('.')[-2]+'.mp4'
            new_file = os.path.join(new_dir,name)
            #cmd = 'ffmpeg -i %s -vcodec libx264 -crf 18 %s' % (os.path.join(dir, file), new_file)
            cmd = 'ffmpeg -i %s -pix_fmt yuv420p %s' % (os.path.join(dir, file), new_file)
            print(cmd)
            subprocess.call(cmd)

fix_file_sizes('D:\\kteender.github.io\\docs\img\\2021-04-18\\cover')