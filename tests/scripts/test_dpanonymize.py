import dpanonymize
from pathlib import Path
import pandas as pd
import tempfile
import json
import string
import os
import shutil

import sys
dpanonymize_root = Path(dpanonymize.__path__[0]).parent
scripts_dir = dpanonymize_root / 'scripts'
test_dir = dpanonymize_root / 'tests'
sys.path.append(str(scripts_dir))
sys.path.append(str(test_dir))


from dpanonymize_test import phoenix_structure, phoenix_structure_BIDS
from dpanonymize_test import Lochness_fake_object, show_tree_then_delete

from bpanon import lock_file, lock_directory


def test_dpanonymize_a_file():
    for datatype in 'mri', 'survey', 'audio', 'video', 'actigraphy':
        in_file = Path(f'{datatype}_temp_file.dcm')
        in_file.touch()

        pii_removed_file = Path('pii_removed_' + in_file.name)

        lock_file(in_file, pii_removed_file, datatype)
        assert pii_removed_file.is_file()

        os.remove(in_file)
        os.remove(pii_removed_file)



def test_dpanonymize_a_directory():
    for datatype in 'mri', 'survey', 'audio', 'video', 'actigraphy':
        temp_dir = Path(f'{datatype}_raw_dir')
        temp_dir.mkdir(exist_ok=True)
        
        in_file = temp_dir / f'{datatype}_temp_file.dcm'
        in_file.touch()

        out_dir = Path(f'{datatype}_pii_removed_dir')

        lock_directory(temp_dir, out_dir, datatype)
        assert out_dir.is_dir()
        assert (out_dir / in_file.name).is_file()

        shutil.rmtree(temp_dir)
        shutil.rmtree(out_dir)




