import zipfile
import shutil


def zip_directory(path, zip_file_path: str):
    """
    zip an entire folder
    """
    import os

    base_name = zip_file_path.replace(".zip", "")
    try:
        os.remove(zip_file_path)
    except Exception as e:
        pass

    print("Making archive: %s" % zip_file_path)
    shutil.make_archive(base_name, "zip", path)
