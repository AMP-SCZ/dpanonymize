import bpanonymize
from pathlib import Path
import pandas as pd
import tempfile
import json
import string

import sys
lochness_root = Path(bpanonymize.__path__[0]).parent
scripts_dir = lochness_root / 'scripts'
test_dir = lochness_root / 'tests'
sys.path.append(str(scripts_dir))
sys.path.append(str(test_dir))


from bpanonymize_test import phoenix_structure, phoenix_structure_BIDS
from bpanonymize_test import Lochness_fake_object, show_tree_then_delete


def test_bpanonymize_nonBIDS(phoenix_structure):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = False
    bpanonymize.lock_lochness(Lochness)

    show_tree_then_delete('tmp_phoenix')


def test_bpanonymize_BIDS(phoenix_structure_BIDS):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = True
    bpanonymize.lock_lochness(Lochness)

    show_tree_then_delete('tmp_phoenix')
