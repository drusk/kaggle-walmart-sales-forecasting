#!/bin/sh
# Usage: unixnl.sh input_file > output_file

sed -e 's//\n/g' $1
