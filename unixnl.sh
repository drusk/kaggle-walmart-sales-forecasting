#!/bin/sh
# Usage: unixnl.sh input_file 

sed -i 's/\r/\n/g' $1
