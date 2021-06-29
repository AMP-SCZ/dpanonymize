import lockness
from pathlib import Path
import pandas as pd
import tempfile
import json
import string

import sys
lochness_root = Path(lockness.__path__[0]).parent
scripts_dir = lochness_root / 'scripts'
test_dir = lochness_root / 'tests'
sys.path.append(str(scripts_dir))
sys.path.append(str(test_dir))


from lockness_test import phoenix_structure, phoenix_structure_BIDS
from lockness_test import Lochness_fake_object, show_tree_then_delete


def test_lockness_nonBIDS(phoenix_structure):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = False
    lockness.lock_lochness(Lochness)

    show_tree_then_delete('tmp_phoenix')


def test_lockness_BIDS(phoenix_structure_BIDS):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = True
    lockness.lock_lochness(Lochness)

    show_tree_then_delete('tmp_phoenix')
