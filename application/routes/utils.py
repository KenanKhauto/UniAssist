import os
import secrets
from PIL import Image
from flask import current_app

def book_hash_user_id(book_name, user_id):
    '''
    This function takes the book name and the user id and returns a hash
    '''
    hash = 0
    for char in book_name:
        hash += ord(char)
    hash += user_id
    return hash


def save_picture(form_picture):
    '''
    This function takes the form picture and saves it in the static/profile_pics folder
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn