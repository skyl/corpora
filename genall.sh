#! /bin/bash
set -e

pushd py
./genall.sh
popd

pushd rs
./genall.sh
popd
