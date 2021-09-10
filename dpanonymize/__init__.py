
from pathlib import Path
import os
import re
from typing import Union, List
import dpanonymize.surveys as SURVEYS
import dpanonymize.actigraphy as ACTIGRAPHY
import dpanonymize.mri as MRI
import dpanonymize.video as VIDEO
import dpanonymize.audio as AUDIO
import dpanonymize.eeg as EEG
import pandas as pd


dtype_module_dict = {
    'surveys': SURVEYS,
    'actigraphy': ACTIGRAPHY,
    'mri': MRI,
    'interviews': VIDEO,
    'audio': AUDIO,
    'video': VIDEO,
    'eeg': EEG
}


class FileInPhoenixBIDS(object):
    '''PHOENIX file class used to grab file information'''
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.dtype = self.file_path.parent.name
        self.subject = self.file_path.parent.parent.name
        self.study = self.file_path.parent.parent.parent.parent.name
        self.general_path = re.sub('/PROTECTED/', '/GENERAL/',
                                   str(self.file_path))

    def anonymize(self, **kwargs) -> None:
        '''Remove PII from the fileInPhoenix object

        Key arguments:
            - self: It should have following attributes
                - self.file_path: path of the file, Path.
                - self.dtype: type of the data, str.
                - self.general_path: path of the target GENERAL path, Path.
                eg) self.file_path = 'PATH/PROTECTED/PATH/TO/FILE'
                    self.dtype = 'surveys'
                    fileInPhoenix.general_path = 'PATH/GENERAL/PATH/TO/FILE'
        '''
        module = dtype_module_dict.get(self.dtype)

        if self.dtype == 'surveys':
            pii_table_loc = kwargs.get('pii_table_loc', False)
            module.process_and_copy_db(
                    pii_table_loc,
                    self.subject,
                    self.file_path,
                    self.general_path)
        else:
            module.remove_pii(self.file_path, self.general_path)

    def __repr__(self):
        return f"<{self.file_path.name} {self.dtype}"


class FileInPhoenix(FileInPhoenixBIDS):
    '''NON-BIDS PHOENIX file class used to grab file information'''
    def __init__(self, file_path):
        super().__init__(file_path)
        self.dtype = self.file_path.parent.parent.name
        self.subject = self.file_path.parent.parent.parent.name


def get_file_objects_from_phoenix(root_dir: Union[Path, str],
                                  BIDS: bool) -> List[FileInPhoenix]:
    '''Search all files under phoenix and get a list of FileInPhoenix objects

    Key Arguments
        - root_dir: 'PROTECTED' directory of PHOENIX structure to search files
                    which are used to create FileInPhoenix objects, str.
        - BIDS: True if the PHOENIX is in BIDS structure, bool.
    '''
    protected_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            full_path = Path(root) / file
            if BIDS:
                protected_files.append(FileInPhoenixBIDS(full_path))
            else:
                protected_files.append(FileInPhoenix(full_path))

    return protected_files


def get_file_objects_from_module(root_dir: Union[Path, str],
                                 module: str,
                                 BIDS: bool) -> List[FileInPhoenix]:
    '''Search all files under phoenix and get a list of FileInPhoenix objects

    Key Arguments:
        - root_dir: 'PROTECTED' directory of PHOENIX structure to search files
                    which are used to create FileInPhoenix objects, str.
        - module: name of the module to remove PII from, str.
        - BIDS: True if the PHOENIX is in BIDS structure, bool.
    '''
    module_dirs = list(root_dir.glob(f'*/*/*/{module}')) if BIDS else \
        list(root_dir.glob(f'*/*/{module}'))

    protected_files = []
    for module_dir in module_dirs:
        protected_files += get_file_objects_from_phoenix(module_dir, BIDS)

    return protected_files


def lock_lochness(Lochness: 'Lochness',
                  module: str = None, **kwargs) -> None:
    '''Lock PII using information from Lochness object

    Requirements:
        - Lochness: Lochness object from lochness.config.load
                    It needs to have 'phoenix_root' (str) and 'BIDS' (bool).
                    eg) Lochness['phoenix_root'] = '/PATH/TO/PHOENIX'
                        Lochness['BIDS'] = True
        - module: name of the datatype to remove PII from, str.
        - expected kwargs:
            - pii_table: Path of the pii process table, which will be used
                         in processing survey data, str.

    '''
    phoenix_root = Path(Lochness['phoenix_root'])
    protected_root = phoenix_root / 'PROTECTED'
    bids = Lochness['BIDS'] if 'BIDS' in Lochness else False

    pii_table_loc = kwargs.get('pii_table_loc', False)
    if not pii_table_loc:
        df = pd.DataFrame({
            'pii_label_string': [
                'address', 'phone_number', 'date',
                'patient_name', 'subject_name'],
            'process': [
                'remove', 'random_number', 'change_date',
                'random_string', 'replace_with_subject_id']
            })
        pii_table_loc = phoenix_root.parent / 'pii_convert.csv'
        df.to_csv(pii_table_loc)
        kwargs['pii_table_loc'] =  pii_table_loc


    # get_file_objects_from_phoenix and get_file_objects_from_module takes
    # PROTECTED path, but FileInPhoenixBIDS and FileInPhoenix are designed
    # to set both GENERAL & PROTECTED paths.
    file_object_list = get_file_objects_from_phoenix(protected_root, bids) \
        if module is None else \
        get_file_objects_from_module(protected_root, module, bids)
    
    for file_object in file_object_list:
        file_object.anonymize(**kwargs)

