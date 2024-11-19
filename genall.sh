#! /bin/bash
set -e

echo "Generating python"
pushd py
./genall.sh
popd

echo "Generating rust"
pushd rs
./genall.sh
popd
