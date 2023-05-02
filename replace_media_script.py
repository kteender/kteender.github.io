
file = 'D:\\kteender.github.io\\_posts\\technical-blog\\backup03.md'

f1 = open(file, 'r', encoding="utf8")
lines = f1.read().split('\n')
new_lines = []
f1.close()

for i in range(0, len(lines)):
    line = lines[i]
    if "https://ktcgart.files.wordpress.com" in line:
        if  ".png" in line or ".jpg" in line:
            s1 = line.split("/")
            name = s1[-1].split("?")[0]
            html_str =   """<div class='captioned-image'>
    <img src='/img/2019-12-18-char-setup-mobu/%s' style='max-width:max-content;'>
    <p>AN IMAGE CAPTION</p>
</div>""" % name
            new_lines.append(html_str)
        elif ".mp4" in line or ".gif":
            s1 = line.split("/")
            name = s1[-1].split("?")[0].split(".")[0]+".mp4"
            html_str = """<div class="captioned-image">
    <video controls autoplay loop muted preload="none">
        <source src="/img/2019-12-18-char-setup-mobu/%s" type="video/mp4" />
    </video>
    <p>A VIDEO CAPTION</p>
</div>""" % name
            new_lines.append(html_str)
    # if "[" and "]" in line:
    #     link_text = line.split("]")[0].split("[")[-1]
    #     if "https://ktcgart.blog" in line:
    #         blog_file = line.split("/")[-2]+".md"
    #         html_str = """<a href="{% link _posts/technical-blog/"""+blog_file+""" %}">"""+link_text+"""</a>"""
    #     else:
    #         link = line.split(")")[0].split(["("])[-1]
    #         html_str = """<a href="%s">%s</a>""" % (link,  link_text)
    else:
        new_lines.append(line)

save_str = "\n".join(new_lines)

new_file = 'D:\\kteender.github.io\\_posts\\technical-blog\\2019-12-18-characterization-and-character-face-setup-in-motionbuilder.md'
f2 = open(new_file, 'w')
f2.write(save_str)
f2.close()

