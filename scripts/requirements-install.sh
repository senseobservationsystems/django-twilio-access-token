#!/bin/bash

RUN_INTERNALLY="$1"

install_app_requirements() {
    if [ -z "$RUN_INTERNALLY" ]; then
        echo "Run installation locally"
    else
        echo "Run installation for travis"
    fi

    # Use virtualenv for internal testing.
    if [ -z "$RUN_INTERNALLY" ]; then
        echo "Preparing virtualenv on your machine..."
        python3 -m venv .venv
        source .venv/bin/activate
        echo ""
    fi

    echo "Installing app requirements..."
    cd test_project
    pip install -r requirements.txt
    pip install flake8
    cd ..
    python setup.py develop
    echo ""
}

install_app_requirements
