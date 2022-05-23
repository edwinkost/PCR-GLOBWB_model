#!/usr/bin/env bash
set -e


# Change these for your specific setup.

#~ # In Kor's development environment:
#~ lue_install_prefix="$LUE_OBJECTS"
#~ hpx_install_prefix="$LUE_OBJECTS/_deps/hpx-build"
#~ 
#~ # On a LUE user's runtime environment:
#~ lue_install_prefix="prefix/of/wherever/you/installed/lue"
#~ hpx_install_prefix="$lue_install_prefix"

# edwin
lue_install_prefix="/home/edwin/opt/lue"
hpx_install_prefix="$lue_install_prefix"

# A tcn node on snellius:
# - 2 packages / node
# - 4 NUMA nodes / package → 8 NUMA nodes
# - 16 CPU cores / NUMA node → 128 CPU cores


#~ export PYTHONPATH=$lue_install_prefix/lib/python3.9
export PYTHONPATH=$lue_install_prefix/lib64/python3.9
export LD_PRELOAD=$EBROOTGPERFTOOLS/lib/libtcmalloc_minimal.so.4


function run_on_snellius_node()

