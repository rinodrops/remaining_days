#!/bin/bash

# =============================================================================
# Download and update syukujitsu.csv file
#
# 1. Download syukujitsu.csv to temporary directory
# 2. Copy it if the download was done successfully
# =============================================================================

# Temporary file location
temp_file="/tmp/syukujitsu.csv"

# Final file location
final_file="syukujitsu.csv"

# Current date
current_date=$(date '+%Y-%m-%d %H:%M:%S')

# -----------------------------------------------------------------------------

# Download the file to the temporary location
curl -s https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv -o "$temp_file"

# Check if the download was successful
if [ $? -eq 0 ]; then
    # If successful, copy the file to the final location
    cp "$temp_file" "$final_file"
else
    # If the download failed, print an error message
    echo "[$current_date] Download failed. File not updated."
fi
