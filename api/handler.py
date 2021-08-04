from api.models import *


def get_albums():
    albums = Album.query.all()
    for album in albums:
        album.images = get_album_images(album.id)
    return albums


def get_album(album_id):
    album = Album.query.filter_by(id=album_id).first()
    if album is not None:
        album.images = get_album_images(album.id)

    return album


def get_album_images(album_id) -> list:
    print(f"Fetching images for {album_id}")
    results = []
    images = Image.query.filter_by(album=album_id).all()
    for image in images:
        results.append(image.as_dict())
    return results
