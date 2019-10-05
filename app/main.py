from os import makedirs, listdir, path as p
from random import choice
from PIL import Image
from flask import Flask, render_template, abort, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/galleries/')
def galleries():
    galleries = []
    galleries_names = listdir('galleries')
    for gallery_name in galleries_names:
        gallery_path = p.join('galleries', gallery_name)
        photos = listdir(gallery_path)
        if photos:
            for i in range(3):
                photo = choice(photos)
                photo_path = p.join(gallery_path, photo)
                if p.isfile(photo_path):
                    break
            galleries.append({
                'name': gallery_name,
                'link': '/' + gallery_path,
                'thumbnail': '/' + photo_path + '?h=280'
            })
    return render_template('galleries.html', galleries=galleries)

@app.route('/galleries/<path:path>')
def images(path):
    path = p.join('galleries', path)
    image = p.basename(path)
    directory = p.dirname(path)
    image_l = image.split('.')
    image_ext = image_l[-1]
    image_name = '.'.join(image_l[:-1])
    if not p.exists(path): abort(400)
    width = request.args.get('w', None)
    height = request.args.get('h', None)
    if width is None and height is None:
        return send_from_directory(directory, image)
    rsz_directory = p.join(directory, 'rsz')
    if not p.exists(rsz_directory):
        makedirs(rsz_directory)
    rsz_image_name = image_name
    if width is not None and width.isdigit():
        rsz_image_name += '_w' + width
    if height is not None and height.isdigit():
        rsz_image_name += '_h' + height
    rsz_image = rsz_image_name + '.' + image_ext
    rsz_path = p.join(rsz_directory, rsz_image)
    if p.exists(rsz_path):
        return send_from_directory(rsz_directory, rsz_image)
    orig_img = Image.open(path)
    w, h = orig_img.size
    if width and height:
        max_size = (int(width), int(height))
    elif width:
        max_size = (int(width), h)
    elif height:
        max_size = (w, int(height))
    else:
        abort(400)
    orig_img.thumbnail(max_size, Image.ANTIALIAS)
    orig_img.save(rsz_path)
    if p.exists(rsz_path):
        return send_from_directory(rsz_directory, rsz_image)
    else:
        abort(404)