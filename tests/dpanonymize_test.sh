#!/usr/bin/env bash

export PYTHONPATH=`pwd`:$PYTHONPATH

# quick tests
pytest dpanonymize_test.py
pytest dpanonymize/test_dpanonymize.py
pytest dpanonymize/test_redcap.py
pytest scripts/test_dpanon.py
