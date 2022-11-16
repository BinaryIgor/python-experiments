import os


def root_dir(root_dir="src"):
    """
    Returns root dir, understood as dir with given directory
     :return: str
    """

    def root_file_path(path):
        return os.path.join(path, root_dir)

    root = os.getcwd()
    while not os.path.isdir(root_file_path(root)):
        root, _ = os.path.split(root)

    return root
