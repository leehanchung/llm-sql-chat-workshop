#!/bin/bash

# URL of the tarball
TARBALL_URL="https://static.crunchbase.com/data_crunchbase/bulk_export_sample.tar.gz"

# Get the parent directory of the current script
PARENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

# Name of the directory to extract tarball into
EXTRACTION_DIR="${PARENT_DIR}/data/source_csv"

# Create the directory if it doesn't exist
mkdir -p "$EXTRACTION_DIR"

# Change to the extraction directory
cd "$EXTRACTION_DIR"

# Download the tarball
wget "$TARBALL_URL" -O tarball.tar.gz

# Extract the tarball
tar -xzvf tarball.tar.gz

# Remove the downloaded tarball
rm tarball.tar.gz
