#!/bin/bash
script_dir=$(dirname $(readlink -f "$0"))
#re-init app
rm $script_dir/notices/*.dat
