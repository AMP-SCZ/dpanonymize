import bpanonymize
from pathlib import Path
import sys
import re
lochness_root = Path(bpanonymize.__path__[0]).parent
scripts_dir = lochness_root / 'scripts'
test_dir = lochness_root / 'tests'
sys.path.append(str(scripts_dir))
sys.path.append(str(test_dir))

from typing import Union
import os

from bpanonymize_test import phoenix_structure


class FileInPhoenixBIDS(object):
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.subject = self.file_path.parent.name
        self.dtype = self.file_path.parent.parent.name
        self.study = self.file_path.parent.parent.parent.name

        self.general = re.sub('/PROTECTED/', '/GENERAL', str(self.file_path))

    def __repr__(self):
        return f"<{self.file_path.name}>"

def get_all_file_objects_from_phoenix(phoenix_root):
    protected_dir = Path(phoenix_root) / 'PROTECTED'

    protected_files = []
    for root, dirs, files in os.walk(protected_dir):
        for f in files:
            full_path = Path(root) / f
            if len(full_path.relative_to(phoenix_root).parts) == 5:
                protected_files.append(FileInPhoenixBIDS(full_path))

    return protected_files



def test_phoenix_structure_class(phoenix_structure):

    protected_files = get_all_file_objects_from_phoenix('tmp_phoenix')

    print(protected_files)
    # print(phoenixStruct.StudyA.survey)
    # print(phoenixStruct.StudyA.survey.subject01)
    # print(phoenixStruct.StudyA.survey.subject01.protected_files)
    # print(dir(phoenixStruct.StudyA.survey.subject01))
    # assert len(phoenixStruct.studies) == 1
    
    # print(phoenixStruct.stu)
    # print(phoenixStruct.datatypes)
    # print(phoenixStruct.subjects)
