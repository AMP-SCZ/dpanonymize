import dpanonymize
from pathlib import Path
import pandas as pd
import tempfile
import json
import string

import sys
lochness_root = Path(dpanonymize.__path__[0]).parent
scripts_dir = lochness_root / 'scripts'
test_dir = lochness_root / 'tests'
sys.path.append(str(scripts_dir))
sys.path.append(str(test_dir))

from dpanonymize_test import phoenix_structure, phoenix_structure_BIDS
from dpanonymize_test import Lochness_fake_object, show_tree_then_delete

from dpanonymize.surveys import read_pii_mapping_to_dict
from dpanonymize.surveys import load_raw_return_proc_json
from dpanonymize.surveys import process_pii_string
from dpanonymize.surveys import get_shuffle_dict_for_type


def test_survey_simple(phoenix_structure):
    show_tree_then_delete('tmp_phoenix')
    pass


def test_survey_simple_BIDS(phoenix_structure_BIDS):
    pass


def test_read_pii_mapping_to_dict_empty():
    assert read_pii_mapping_to_dict('') == {}


def test_read_pii_mapping_to_dict_one_line():
    df = pd.DataFrame({
        'pii_label_string': ['address'],
        'process': 'remove'
        })

    with tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.csv') as tmpfilename:
        df.to_csv(tmpfilename.name)

    d = read_pii_mapping_to_dict(tmpfilename.name)
    assert d == {'address': 'remove'}


def test_read_pii_mapping_to_dict_two_line():
    df = pd.DataFrame({
        'pii_label_string': ['address', 'phone_number'],
        'process': ['remove', 'random_number']
        })

    with tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.csv') as tmpfilename:
        df.to_csv(tmpfilename.name)

    d = read_pii_mapping_to_dict(tmpfilename.name)
    assert d == {'address': 'remove',
                 'phone_number': 'random_number'}


def get_pii_mapping_table():
    df = pd.DataFrame({
        'pii_label_string': ['address', 'phone_number'],
        'process': ['remove', 'random_number']
        })

    with tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.csv') as tmpfilename:
        df.to_csv(tmpfilename.name)

    return tmpfilename.name


def get_json_file():
    d = [{'subject': 'test',
          'address': 'Boston, 02215',
          'phone_number': '877-000-0000',
          'ha_phone_number': '800-000-0000'}]

    with tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.json') as tmpfilename:
        with open(tmpfilename.name, 'w') as f:
            json.dump(d, f)

    return tmpfilename.name


def test_load_raw_return_proc_json():
    print()
    json_loc = get_json_file()
    pii_table_loc = get_pii_mapping_table()

    pii_str_proc_dict = read_pii_mapping_to_dict(pii_table_loc)
    processed_content = load_raw_return_proc_json(json_loc,
                                                  pii_str_proc_dict,
                                                  'subject01')

    assert type(processed_content) == bytes


def test_process_pii_string():
    print(process_pii_string('my name is kevin', 'random_string', 'subject01'))
    print(process_pii_string('1923956', 'random_number', 'subject01'))
    print(process_pii_string('816-198-963', 'random_number', 'subject01'))
    print(process_pii_string('Kevin Cho', 'replace_with_subject_id',
                             'kevin2subject01'))


def test_get_shuffle_dict_for_type():
    print(get_shuffle_dict_for_type(string.digits, '393jfi'))
    print(get_shuffle_dict_for_type(string.ascii_lowercase, '393jfiefy090'))
    print(get_shuffle_dict_for_type(string.ascii_uppercase, '393jfUUy090'))

