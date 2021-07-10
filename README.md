# dpanonymize

`dpanonymize` is a PII removal tool for given data types. It's mainly designed
to work with `lochness` on a PHOENIX structured data, but it also has
functionalities to take separate file and folder with predefined datatype.

   * [Installation](#installation)
   * [Debugging](#debugging)
   * [Tests](#tests)
   * [Running](#running)
   * [Documentation](#documentation)


## Installation

Just use `pip`:

```
pip install dpanonymize
```


For most recent DPACC-lochness:

```
pip install git+https://github.com/AMP-SCZ/dpanonymize
```


## Debugging

```
cd ~
git clone https://github.com/AMP-SCZ/dpanonymize
cd dpanonymize
pip install .
```

If you do not have `lochness` installed already:

```
pip install git+https://github.com/AMP-SCZ/lochness
```

## Tests

```
cd dpanonymize/tests
./dpanonymize_test.sh
```


## Running

- Execute PII removal from `lochness`(`sync.py`)
  
  TBD

- Execute PII removal on a PHOENIX folder
```
# apply PII removal in all datatypes
dpanon.py --phoenix_root /path/to/PHOENIX

# or you can also select which datatype to apply PII removal
dpanon.py --phoenix_root /path/to/PHOENIX --datatype actigraphy
dpanon.py --phoenix_root /path/to/PHOENIX --datatype surveys
```

- Execute PII removal on a single file
```
dpanon.py \
    --in_file /path/to/surveys/file \
    --out_file /path/to/PII_removed/file \
    --datatype surveys
```

- Execute PII removal on a directory where there are multiple files of same data type

  This applies PII removal on all files under the given directory.
```
dpanon.py \
    --in_dir /path/to/surveys/directory \
    --out_dir /path/to/PII_removed/directory \
    --datatype surveys
```



## Documentation

TBD
