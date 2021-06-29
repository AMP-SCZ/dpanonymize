import pandas as pd
from pathlib import Path
import pytest
import json
import string
import os
import shutil



class PhoenixStructure(object):
    '''Phoenix structure object'''
    def __init__(self, phoenix_root, BIDS=True):
        self.phoenix_root = Path(phoenix_root)
        self.studies = ['StudyA']
        self.bids = BIDS
        self.general_folder = self.phoenix_root / 'GENERAL'
        self.protected_folder = self.phoenix_root / 'PROTECTED'

        self.study_subject_dict = {
                'StudyA': ['subject01', 'subject02', 'subject03'],
                'StudyB': ['subject01', 'subject02', 'subject03']
                }

    def create_fake_protected_redcap(self):
        for study in self.studies:
            for subject in self.study_subject_dict[study]:
                study_dir = self.protected_folder / study

                if self.bids:
                    survey_dir = study_dir / 'survey' / subject
                    survey_dir.mkdir(exist_ok=True, parents=True)
                    subject_json = survey_dir / (f'{subject}.{study}.json')

                    # create json with pii
                    d = [{subject: 'test',
                          'address': 'Boston, 02215',
                          'phone_number': '877-000-0000',
                          'ha_phone_number': '800-000-0000'}]

                    with open(subject_json, 'w') as f:
                        json.dump(d, f)
                else:
                    survey_dir = study_dir / subject / 'survey'
                    survey_dir.mkdir(exist_ok=True, parents=True)
                    subject_json = survey_dir / (f'{subject}.{study}.json')

                    # create json with pii
                    d = [{subject: 'test',
                          'address': 'Boston, 02215',
                          'phone_number': '877-000-0000',
                          'ha_phone_number': '800-000-0000'}]

                    with open(subject_json, 'w') as f:
                        json.dump(d, f)


    def create_fake_repo(self, var, file_extension):
        for study in self.studies:
            for subject in self.study_subject_dict[study]:
                study_dir = self.protected_folder / study
                var_dir = study_dir / var / subject if self.bids \
                        else study_dir / subject / var
                var_dir.mkdir(exist_ok=True, parents=True)

                # subjects = self.study_subject_dict[study]

                # for subject in subjects:
                subject_data = var_dir / \
                        (f'{subject}.{study}.{file_extension}')

                subject_data.touch(exist_ok=True)


def Lochness_fake_object(phoenix_root):
    Lochness = {}
    Lochness['phoenix_root'] = phoenix_root
    return Lochness


def show_tree_then_delete(tmp_dir):
    print()
    print('-'*75)
    print(f'Temporary directory structure : {tmp_dir}')
    print('-'*75)
    print(os.popen(f'tree {tmp_dir}').read())
    shutil.rmtree(tmp_dir)


@pytest.fixture
def phoenix_structure():
    phoenix_root = 'tmp_phoenix'
    phoenix_structure = PhoenixStructure(phoenix_root, BIDS=False)
    phoenix_structure.create_fake_protected_redcap()
    phoenix_structure.create_fake_repo('mri', 'dcm')
    phoenix_structure.create_fake_repo('interviews', 'mp4')
    phoenix_structure.create_fake_repo('actigraphy', 'csv')
    
@pytest.fixture
def phoenix_structure_BIDS():
    phoenix_root = 'tmp_phoenix'
    phoenix_structure = PhoenixStructure(phoenix_root, BIDS=True)
    phoenix_structure.create_fake_protected_redcap()
    phoenix_structure.create_fake_repo('mri', 'dcm')
    phoenix_structure.create_fake_repo('interviews', 'mp4')
    phoenix_structure.create_fake_repo('actigraphy', 'csv')

def test_test_phoenix_structure_short(phoenix_structure):
    show_tree_then_delete('tmp_phoenix')


def test_test_phoenix_structure_BIDS(phoenix_structure_BIDS):
    show_tree_then_delete('tmp_phoenix')


# def test_read_pii_mapping_to_dict_empty():
    # assert read_pii_mapping_to_dict('') == {}


# def test_read_pii_mapping_to_dict_one_line():
    # df = pd.DataFrame({
        # 'pii_label_string': ['address'],
        # 'process': 'remove'
        # })

    # with tempfile.NamedTemporaryFile(
            # delete=False,
            # suffix='.csv') as tmpfilename:
        # df.to_csv(tmpfilename.name)

    # d = read_pii_mapping_to_dict(tmpfilename.name)
    # assert d == {'address': 'remove'}


# def test_read_pii_mapping_to_dict_two_line():
    # df = pd.DataFrame({
        # 'pii_label_string': ['address', 'phone_number'],
        # 'process': ['remove', 'random_number']
        # })

    # with tempfile.NamedTemporaryFile(
            # delete=False,
            # suffix='.csv') as tmpfilename:
        # df.to_csv(tmpfilename.name)

    # d = read_pii_mapping_to_dict(tmpfilename.name)
    # assert d == {'address': 'remove',
                 # 'phone_number': 'random_number'}


# def get_pii_mapping_table():
    # df = pd.DataFrame({
        # 'pii_label_string': ['address', 'phone_number'],
        # 'process': ['remove', 'random_number']
        # })

    # with tempfile.NamedTemporaryFile(
            # delete=False,
            # suffix='.csv') as tmpfilename:
        # df.to_csv(tmpfilename.name)

    # return tmpfilename.name


# def get_json_file():
    # d = [{'subject': 'test',
          # 'address': 'Boston, 02215',
          # 'phone_number': '877-000-0000',
          # 'ha_phone_number': '800-000-0000'}]

    # with tempfile.NamedTemporaryFile(
            # delete=False,
            # suffix='.json') as tmpfilename:
        # with open(tmpfilename.name, 'w') as f:
            # json.dump(d, f)

    # return tmpfilename.name


# def test_load_raw_return_proc_json():
    # print()
    # json_loc = get_json_file()
    # pii_table_loc = get_pii_mapping_table()

    # pii_str_proc_dict = read_pii_mapping_to_dict(pii_table_loc)
    # processed_content = load_raw_return_proc_json(json_loc,
                                                  # pii_str_proc_dict,
                                                  # 'subject01')

    # assert type(processed_content) == bytes


# def test_process_pii_string():
    # print(process_pii_string('my name is kevin', 'random_string', 'subject01'))
    # print(process_pii_string('1923956', 'random_number', 'subject01'))
    # print(process_pii_string('816-198-963', 'random_number', 'subject01'))
    # print(process_pii_string('Kevin Cho', 'replace_with_subject_id',
                             # 'kevin2subject01'))


# def test_get_shuffle_dict_for_type():
    # print(get_shuffle_dict_for_type(string.digits, '393jfi'))
    # print(get_shuffle_dict_for_type(string.ascii_lowercase, '393jfiefy090'))
    # print(get_shuffle_dict_for_type(string.ascii_uppercase, '393jfUUy090'))

