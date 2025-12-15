import os
import sys
import types

import mapof.core.utils as utils

VECTOR = [1, 2, 3, 4]


def test_make_folder(tmp_path):
    utils.make_folder_if_do_not_exist(tmp_path / "test_folder")
    assert os.path.isdir(tmp_path / "test_folder") == True


def test_rotate_vector_zero():
    vector = VECTOR
    assert vector == utils.rotate(vector, 0)


def test_rotate_vector_length():
    vector = VECTOR
    assert vector == utils.rotate(vector, 4)


def test_rotate_vector_two():
    vector = VECTOR
    rotated = utils.rotate(vector, 2)
    assert rotated == [3, 4, 1, 2]


def test_rotate_vector_two_over_length():
    vector = VECTOR
    rotated = utils.rotate(vector, 6)
    assert rotated == [3, 4, 1, 2]


def test_get_instance_id_single_family():
    assert utils.get_instance_id(True, "famA", 5) == "famA"


def test_get_instance_id_multi_family():
    assert utils.get_instance_id(False, "famB", 3) == "famB_3"


def test_is_module_loaded_roundtrip():
    module_name = "mapof_dummy_module"
    if module_name in sys.modules:
        del sys.modules[module_name]
    assert utils.is_module_loaded(module_name) is False
    sys.modules[module_name] = types.ModuleType(module_name)
    try:
        assert utils.is_module_loaded(module_name) is True
    finally:
        sys.modules.pop(module_name, None)
