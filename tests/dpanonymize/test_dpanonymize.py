import dpanonymize
from pathlib import Path
import pandas as pd
import tempfile
import json
import string

import sys
dpanonymize_root = Path(dpanonymize.__path__[0]).parent
scripts_dir = dpanonymize_root / 'scripts'
test_dir = dpanonymize_root / 'tests'
sys.path.append(str(scripts_dir))
sys.path.append(str(test_dir))


from dpanonymize_test import phoenix_structure, phoenix_structure_BIDS
from dpanonymize_test import phoenix_structure_BIDS_processed
from dpanonymize_test import Lochness_fake_object, show_tree_then_delete


def test_dpanonymize_nonBIDS(phoenix_structure):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = False
    dpanonymize.lock_lochness(Lochness)

    show_tree_then_delete('tmp_phoenix')


def test_dpanonymize_BIDS(phoenix_structure_BIDS):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = True
    dpanonymize.lock_lochness(Lochness)

    show_tree_then_delete('tmp_phoenix')


def test_dpanonymize_module_nonBIDS(phoenix_structure):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = False
    dpanonymize.lock_lochness(Lochness, module='survey')

    show_tree_then_delete('tmp_phoenix')


def test_dpanonymize_module_BIDS(phoenix_structure_BIDS):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = True
    dpanonymize.lock_lochness(Lochness, module='survey')

    show_tree_then_delete('tmp_phoenix')


def test_dpanonymize_processed_raw_mixed_BIDS(phoenix_structure_BIDS_processed):
    Lochness = Lochness_fake_object('tmp_phoenix')
    Lochness['BIDS'] = True
    dpanonymize.lock_lochness(Lochness)

    show_tree_then_delete('tmp_phoenix')
