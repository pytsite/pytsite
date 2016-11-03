"""PytSite ODM File Storage Event Handlers.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _update_0_90_0():
    import re, os, shutil
    from pytsite import db, reg, logger

    path_re = re.compile('^image/')

    # Rename existing 'images' collection to 'file_images'
    collection_names = db.get_collection_names()
    if 'file_images' not in collection_names and 'images' in collection_names:
        db.get_collection('images').rename('file_images')
        msg = "Collection 'images' renamed to 'file_images'"
        logger.info(msg)

        images = db.get_collection('file_images')
        for doc in images.find():
            images.update_one({'_id': doc['_id']}, {
                '$set': {
                    'path': path_re.sub('file/image/', doc['path'])
                }
            })
            msg = 'Path updated for image: {}'.format(doc['_id'])
            logger.info(msg)

    # Move 'storage/image' to 'storage/file/image'
    images_dir = os.path.join(reg.get('paths.storage'), 'image')
    if os.path.exists(images_dir):
        files_dir = os.path.join(reg.get('paths.storage'), 'file')

        if not os.path.exists(files_dir):
            os.makedirs(files_dir, 0o755)

        shutil.move(images_dir, files_dir)

        msg = '{} moved to {}.'.format(images_dir, files_dir)
        logger.info(msg)


def update(version: str):
    if version == '0.90.0':
        _update_0_90_0()
