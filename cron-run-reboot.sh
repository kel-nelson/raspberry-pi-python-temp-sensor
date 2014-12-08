#!/bin/bash
script_dir=$(dirname $(readlink -f "$0"))
#re-init app
rm $script_dir/last_report_notice.dat $script_dir/last_error_notice.dat
