from pathlib import Path
import shutil
from typing import List

def remove_pii(data_in: List[str, Path], data_out: List[str, Path]):
    '''Remove PII from actigraphy data - place holder'''
    shutil.copy(data_in, data_out)

