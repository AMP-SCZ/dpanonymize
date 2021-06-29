from pathlib import Path
import shutil
from typing import Union

def remove_pii(data_in: Union[str, Path], data_out: Union[str, Path]):
    '''Remove PII from MRI data - place holder'''
    if not Path(data_out).parent.is_dir():
        Path(data_out).parent.mkdir(parents=True)
    shutil.copy(data_in, data_out)

