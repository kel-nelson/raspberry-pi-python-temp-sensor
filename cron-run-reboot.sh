#!/bin/bash
script_dir=$(dirname $(readlink -f "$0"))
#re-init app
rm -f $script_dir/notices/*.dat
