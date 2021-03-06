import dpanonymize
from pathlib import Path
import pandas as pd
import tempfile
import json
import string
import os
import shutil
import pytest

import sys
dpanonymize_root = Path(dpanonymize.__path__[0]).parent
scripts_dir = dpanonymize_root / 'scripts'
test_dir = dpanonymize_root / 'tests'
sys.path.append(str(scripts_dir))
sys.path.append(str(test_dir))


from dpanonymize_test import phoenix_structure, phoenix_structure_BIDS
from dpanonymize_test import Lochness_fake_object, show_tree_then_delete

from dpanon import lock_file, lock_directory, parse_args, dpanonymize


def test_dpanonymize_a_file():
    for datatype in 'mri', 'audio', 'video', 'actigraphy':
        in_file = Path(f'{datatype}_temp_file.dcm')
        in_file.touch()

        pii_removed_file = Path('pii_removed_' + in_file.name)

        lock_file(in_file, pii_removed_file, datatype)
        assert pii_removed_file.is_file()

        os.remove(in_file)
        os.remove(pii_removed_file)


def test_dpanonymize_a_directory():
    for datatype in 'mri', 'audio', 'video', 'actigraphy':
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


def test_parser():
    # with datatype
    args = parse_args(['-p', 'tmp_phoenix',
                       '-dt', 'surveys'])
    print(args)


def test_phoenix_root_non_bids_with_dt(phoenix_structure):
    # with datatype
    args = parse_args(
            ['-p', 'tmp_phoenix',
             '-dt', 'surveys',
             '-pt', '/Users/kc244/dpanonymize/tests/pii_convert.csv'])

    dpanonymize(args)
    show_tree_then_delete('tmp_phoenix')


def test_phoenix_root_bids_with_dt(phoenix_structure_BIDS):
    # with datatype
    args = parse_args(
            ['-p', 'tmp_phoenix',
             '-dt', 'surveys',
             '-pt', '/Users/kc244/dpanonymize/tests/pii_convert.csv',
             '-b'])

    dpanonymize(args)
    show_tree_then_delete('tmp_phoenix')


def test_file_with_dt():
    for datatype in 'mri', 'surveys', 'audio', 'video', 'actigraphy':
        in_file = Path(f'{datatype}_temp_file.json')
        in_file.touch()

        pii_removed_file = Path('pii_removed_' + in_file.name)

        # with datatype
        args = parse_args(
                ['-i', str(in_file),
                 '-o', str(pii_removed_file),
                 '-pt', '/Users/kc244/dpanonymize/tests/pii_convert.csv',
                 '-dt', datatype])
        dpanonymize(args)
        assert pii_removed_file.is_file()

        os.remove(in_file)
        os.remove(pii_removed_file)


def test_dir_with_dt():
    for datatype in 'mri', 'surveys', 'audio', 'video', 'actigraphy':
        temp_dir = Path(f'{datatype}_raw_dir')
        temp_dir.mkdir(exist_ok=True)
        
        in_file = temp_dir / f'{datatype}_temp_file.json'
        in_file.touch()

        out_dir = Path(f'{datatype}_pii_removed_dir')

        args = parse_args(
                ['-id', str(temp_dir),
                 '-od', str(out_dir),
                 '-pt', '/Users/kc244/dpanonymize/tests/pii_convert.csv',
                 '-dt', datatype])
        dpanonymize(args)
        assert out_dir.is_dir()
        assert (out_dir / in_file.name).is_file()

        shutil.rmtree(temp_dir)
        shutil.rmtree(out_dir)


def test_phoenix_root_bids_with_wrong_dt(phoenix_structure_BIDS):
    # with datatype
    with pytest.raises(SystemExit):
        args = parse_args(['-p', 'tmp_phoenix',
                           '-dt', 'haha',
                           '-b'])

        dpanonymize(args)


def test_phoenix_root_only():
    args = parse_args(['-p', 'tmp_phoenix'])


def test_file_only():
    with pytest.raises(SystemExit):
        args = parse_args(['-i', 'tmp_file'])


def test_dir_only():
    with pytest.raises(SystemExit):
    # with datatype
        args = parse_args(['-id', 'tmp_dir'])


def test_argparse(phoenix_structure_BIDS):
    command = f'{scripts_dir}/dpanon.py -p tmp_phoenix -b'
    os.popen(command).read()
    show_tree_then_delete('tmp_phoenix')
