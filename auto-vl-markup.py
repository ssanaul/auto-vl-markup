import csv, os
def sort_images(dir):
    images = os.listdir(dir)
    sorted_images = [None for image in images]
    for image in images:
        #e.g., 1-2-1_Slide20.png
        ext = image.split('.')[1] #print(ext) => png
        name = image.split('.'+ext)[0] #print(name) => 1-2-1_Slide20
        num = int(name.split('Slide')[1]) #print(num) => 20
        sorted_images[num-1] = name+"."+ext
    return sorted_images
def collect_content(csv_file, image_arr):
    tags = []
    with open(csv_file) as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i >= 1:
                vl_content = {
                    row[0] and row[1]: create_titles(row[0], row[1]),
                    row[2]: create_h2(row[2], i),
                    row[3]: create_h3(row[3], i),
                    row[4]: create_medialink(row[4], row[3]),
                    row[5]: create_slide_tags(row[5], image_arr[i-1], i),
                    row[6]: create_h5(row[6])
                }
                for key in vl_content:
                    if key:
                        tags.append(vl_content[key])
            i += 1
    return tags
def generate_html(csv_file, images_dir, html_file):
    end_tags = '</div>\n'+\
    '<script src="https://ssanaul.github.io/generate-video-lecture-toc.js"></script>\n'+\
    '<script src="https://ssanaul.github.io/query-initialisms.min.js"></script>\n'+\
    '<script src="https://ssanaul.github.io/axe-for-elearning.js"></script>\n'+\
    '</body>\n</html>'
    with open(html_file, 'w') as html:
        for content in collect_content(csv_file, sort_images(images_dir)):
            html.write(content)
        html.write(end_tags)
def create_titles(course_title, module_num):
    return '<!doctype html>\n<html lang="en">\n'+\
            '<head>\n<meta charset="utf-8">\n'+\
    		'<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">\n'+\
            '<title>Module '+module_num+' '+course_title+'</title>\n<link rel="stylesheet" '+\
            'type="text/css" href="eLearningStyle.css">\n<script type="text/javascript" '+\
            'src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML" '+\
            'async></script>\n</head>\n<body>\n<div role="main">\n'+\
            '<h1>Module '+module_num+' '+course_title+'</h1>\n'
def create_h2(lesson, id_iter):
    return '<h2 id="h2_'+str(id_iter)+'">'+lesson+'</h2>\n'
def create_h3(sublesson, id_iter):
    return '<h3 id="h3_'+str(id_iter)+'">'+sublesson+'</h3>\n'
def create_medialink(kaltura_link, sublesson):
    return '<p>\n<a href="'+kaltura_link+'" target="_blank" aria-label="View '+sublesson+' in a new window">\n'+\
    'Media Player for Video\n<img src="Images/new-window.png" alt="Opens in a new window" width="13" height="13"/>\n</a>\n</p>\n'
def create_slide_tags(slide_title, src, id_iter):
    return '<h4>'+slide_title+' - Slide '+str(id_iter)+'</h4>'+'\n<img src="Images/'+src+'" width="450" height="250" alt="">\n'
def create_h5(transcript):
    return '<h5>'+transcript+'</h5>\n'
if __name__ == "__main__":
    generate_html('vl-sheet.csv', 'Images', 'output.html')
