#!/usr/bin/env python

from pathlib import Path
import argparse as ap
import sys
from typing import Union, List
from dpanonymize import dtype_module_dict
import dpanonymize.surveys as SURVEYS
import dpanonymize as dpanon

'''
dpanonymize is designed to be executed from lochness, but this simple shell
executable script is added to use PII removal functionalities of dpanonymize
from shell.
'''

def lock_file(in_file: Union[Path, str],
              out_file: Union[Path, str],
              datatype: str) -> None:
    '''Remove PII using information from a file

    Requirements:
        - in_file: input file path, Path or str
        - out_file: path to save the PII removed file, Path or str
        - datatype: datatype that this in_file belongs to, str
            - 'surveys', 'video', 'audio', 'actigraphy', 'mri', 'eeg'
    '''
    module = dtype_module_dict.get(datatype)
    module.remove_pii(in_file, out_file)


def lock_directory(in_dir: Union[Path, str],
                   out_dir: Union[Path, str],
                   datatype: str, **kwargs) -> None:
    '''Remove PII from all files under a directory

    Requirements:
        - in_file: input directory path, Path or str
        - out_file: directory to save the PII removed file, Path or str
        - datatype: datatype that all of the files belongs to, str
            - 'surveys', 'video', 'audio', 'actigraphy', 'mri', 'eeg'
    '''
    module = dtype_module_dict.get(datatype)

    for in_file in Path(in_dir).glob('*'):
        if in_file.is_file():
            out_file = Path(out_dir) / in_file.name
            if datatype == 'surveys':
                pii_table_loc = kwargs.get('pii_table_loc', False)
                # using the file name without extension as the subject_id input
                # for the process_and_copy_db function
                SURVEYS.process_and_copy_db(
                        pii_table_loc,
                        in_file.name.split('.')[0],
                        in_file,
                        out_file)
            else:
                module.remove_pii(in_file, out_file)


def parse_args(argv):
    '''Parse inputs coming from the terminal'''
    parser = ap.ArgumentParser(description='dpanonymize: PII remover')

    parser.add_argument('-p', '--phoenix_root',
                        type=str,
                        help='Root of PHOENIX directory. If this option is '
                             'given, -i, -o, -d, -od are ignored')
    parser.add_argument('-b', '--bids', action='store_true',
                        help='Option to use if the PHOENIX is in BIDS')
    parser.add_argument('-i', '--in_file', help='A file to remove PII from')
    parser.add_argument('-o', '--out_file',
                        help='PII removed output file path')
    parser.add_argument('-id', '--in_dir',
                        help='A directory to remove PII from')
    parser.add_argument('-od', '--out_dir',
                        help='PII removed output dir path')
    parser.add_argument(
            '-dt', '--datatype',
            choices=['surveys', 'video', 'audio', 'actigraphy', 'mri', 'eeg'],
            help='Datatype to remove PII (applies to -p, -i).')
    parser.add_argument(
            '-ptl', '--pii_table_loc', default=False,
            help='Location of PII table for survey data processing')

    args = parser.parse_args(argv)

    if args.in_file and args.datatype is None:
        parser.error('--in_file and --datatype always appear together')

    if args.in_dir and args.datatype is None:
        parser.error('--in_file and --datatype always appear together')

    return args


def dpanonymize(args):
    if args.phoenix_root:
        in_dict = {'phoenix_root': args.phoenix_root, 'BIDS': args.bids}
        dpanon.lock_lochness(in_dict, args.datatype,
                             pii_table_loc=args.pii_table_loc)

    else:
        if args.in_file:
            if args.datatype == 'surveys':
                print('hahah')
                SURVEYS.process_and_copy_db(
                        args.pii_table_loc,
                        Path(args.in_file).name.split('.')[0],
                        args.in_file,
                        args.out_file)
            else:
                lock_file(args.in_file, args.out_file, args.datatype)

        if args.in_dir:
            lock_directory(args.in_dir, args.out_dir, args.datatype,
                           pii_table_loc=args.pii_table_loc)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    dpanonymize(args)
