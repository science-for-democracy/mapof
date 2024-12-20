import os


def make_folder_if_do_not_exist(path) -> None:
    """
    Create a folder if it does not exist.

    Parameters
    ----------
        path : str
            Path to the folder.

    Returns
    -------
        None
    """
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)


def is_module_loaded(module_import_name):
    """
    Checks if a given module has already been loaded.
    BEWARE: the argument should be the true name of a module, not an alias. That
    is for
    > import foo as bar
    one should pass "foo" to this function
    """
    import sys

    return module_import_name in sys.modules


def get_instance_id(single, family_id, j) -> str:
    """Return the instance id"""
    if single:
        return family_id
    return f"{family_id}_{j}"


def rotate(vector, shift):
    """Rotate a vector"""
    shift = shift % len(vector)
    return vector[shift:] + vector[:shift]
