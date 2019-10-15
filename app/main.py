from os import makedirs, listdir, path as p
from PIL import Image
from flask import Flask, render_template, abort, request, send_from_directory
from lib import getUri

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
        gallery_uri = getUri(gallery_name)
        photos = listdir(gallery_path)
        if not photos: continue
        if 'thumbnail.jpg' not in photos: continue
        galleries.append({
            'name': gallery_name,
            'link': '/galleries/{gallery}/'.format(gallery=gallery_uri),
            'thumbnail': '/img/{gallery}/thumbnail.jpg?h=280'.format(gallery=gallery_uri)
        })
    return render_template('galleries.html', galleries=galleries)

@app.route('/galleries/<path:gallery_uri>')
def gallery(gallery_uri):
    for gallery_name in listdir('galleries'):
        if gallery_uri == getUri(gallery_name):
            gallery_path = p.join('galleries', gallery_name)
            if not p.exists(gallery_path): abort(404)
            gallery = {
                'name': gallery_name,
                'photos': []
            }
            photos_list = listdir(gallery_path)
            for photo in photos_list:
                photo_path = p.join(gallery_path, photo)
                if not p.isfile(photo_path): continue
                gallery['photos'].append({
                    'title': photo,
                    'src': '/img/' + photo_path + '?w=280'
                })
            return render_template('gallery.html', gallery=gallery)
    abort(404)

@app.route('/img/galleries/<path:path>')
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