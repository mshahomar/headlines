import os


BASE_DIR = os.getcwd()


def get_app_id(filename):
    app_file = BASE_DIR + "/" + filename
    with open(app_file) as f:
        app_id = f.read()
    
    return app_id