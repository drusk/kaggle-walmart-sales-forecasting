#!/bin/sh
# Usage: unixnl.sh input_file output_file

tr '\r' '\n' < $1 > $2
