
from pathlib import Path
from typing import Union, List
import lockness.survey as SURVEY
import lockness.actigraphy as ACTIGRAPHY
import lockness.mri as MRI
import lockness.video as VIDEO
import lockness.audio as AUDIO
import os
import re


dtype_module_dict = {
    'survey': SURVEY,
    'actigraphy': ACTIGRAPHY,
    'mri': MRI,
    'interviews': VIDEO,
    'audio': AUDIO
}


class FileInPhoenixBIDS(object):
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.subject = self.file_path.parent.name
        self.dtype = self.file_path.parent.parent.name
        self.study = self.file_path.parent.parent.parent.name
        self.general_path = re.sub('/PROTECTED/', '/GENERAL/',
                                   str(self.file_path))

    def __repr__(self):
        return f"<{self.file_path.name}>"


class FileInPhoenix(FileInPhoenixBIDS):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.dtype = self.file_path.parent.name
        self.subject = self.file_path.parent.parent.name


def get_all_file_objects_from_phoenix(phoenix_root: Union[Path, str],
                                      BIDS: bool) -> List[FileInPhoenixBIDS]:
    protected_dir = Path(phoenix_root) / 'PROTECTED'

    protected_files = []
    for root, _, files in os.walk(protected_dir):
        for file in files:
            full_path = Path(root) / file
            if len(full_path.relative_to(phoenix_root).parts) == 5:
                if BIDS:
                    protected_files.append(FileInPhoenixBIDS(full_path))
                else:
                    protected_files.append(FileInPhoenix(full_path))

    return protected_files


def lock_lochness(Lochness: 'Lochness object') -> None:
    '''Lock PII using information from Lochness object

    Requirements:
        - Lochness: Lochness object from lochness.config.load
                    It needs to have 'phoenix_root' (str) and 'BIDS' (bool).
                    eg) Lochness['phoenix_root'] = '/PATH/TO/PHOENIX'
                        Lochness['BIDS'] = True
    '''
    phoenix_root = Lochness['phoenix_root']
    bids = Lochness['BIDS'] if 'BIDS' in Lochness else False

    file_object_list = get_all_file_objects_from_phoenix(phoenix_root, bids)
    for file_object in file_object_list:
        lock_fileInPhoenix(file_object)


def lock_fileInPhoenix(fileInPhoenix: FileInPhoenixBIDS) -> None:
    '''Remove PII from the fileInPhoenix object

    Key arguments:
        - fileInPhoenix: FileInPhoenix or FileInPhoenixBIDS object. It should
                         have following attributes
            - file_path: path of the file, Path.
            - dtype: type of the data, str.
            - general_path: path of the target GENERAL path, Path.
            eg) fileInPhoenix['file_path'] = 'PATH/PROTECTED/PATH/TO/FILE'
                fileInPhoenix['dtype'] = 'survey'
                fileInPhoenix['general_path'] = 'PATH/GENERAL/PATH/TO/FILE'
    '''
    module = dtype_module_dict.get(fileInPhoenix.dtype)
    module.remove_pii(fileInPhoenix.file_path,
                      fileInPhoenix.general_path)

