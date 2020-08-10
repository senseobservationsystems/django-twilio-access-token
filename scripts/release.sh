#!/bin/bash

RUN_INTERNALLY="$1"

prepare_release_dist() {
    if [ -z "$RUN_INTERNALLY" ]; then
        echo "Run release distribution locally"
        source .venv/bin/activate
    fi

    pip install twine
    pip install wheel
    python setup.py bdist_wheel
    python setup.py sdist --formats=gztar
}

upload_dist_to_test_pypi() {
    python -m twine upload --repository testpypi dist/*
}

upload_dist_to_pypi() {
    python -m twine upload dist/*
}

prepare_release_dist
# once you're sure it successfully uploaded to your test repository
# then you may go with uploading distribution code to your pypi repository
# by running `upload_dist_to_pypi`
upload_dist_to_test_pypi
