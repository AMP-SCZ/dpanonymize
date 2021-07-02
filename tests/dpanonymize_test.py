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

    def create_fake_protected_redcap(self, processed=False):
        for study in self.studies:
            for subject in self.study_subject_dict[study]:
                study_dir = self.protected_folder / study

                if self.bids:
                    survey_dir = study_dir / 'survey' / 'processed' / subject \
                        if processed else study_dir / 'survey' / 'raw' / subject
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
                    survey_dir = study_dir / subject / 'survey' / 'processed' \
                            if processed else \
                            study_dir / subject / 'survey' / 'raw'

                    survey_dir.mkdir(exist_ok=True, parents=True)
                    subject_json = survey_dir / (f'{subject}.{study}.json')

                    # create json with pii
                    d = [{subject: 'test',
                          'address': 'Boston, 02215',
                          'phone_number': '877-000-0000',
                          'ha_phone_number': '800-000-0000'}]

                    with open(subject_json, 'w') as f:
                        json.dump(d, f)


    def create_fake_repo(self, var, file_extension, processed=False):
        for study in self.studies:
            for subject in self.study_subject_dict[study]:
                study_dir = self.protected_folder / study
                if self.bids:
                    var_dir = study_dir / var / 'processed' / subject \
                            if processed else \
                            study_dir / var / 'raw' / subject

                else:
                    var_dir = study_dir / subject / var / 'processed' \
                            if processed else \
                            study_dir / subject / var / 'raw'

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

