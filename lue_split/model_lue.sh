#!/usr/bin/env bash
set -e

# edwin
lue_install_prefix="/home/edwin/opt/lue"
hpx_install_prefix="$lue_install_prefix"

# A tcn node on snellius:
# - 2 packages / node
# - 4 NUMA nodes / package → 8 NUMA nodes
# - 16 CPU cores / NUMA node → 128 CPU cores

# We want a process per NUMA node:
# - ntasks: $nr_numa_nodes
# - cpus-per-task: 16

export PYTHONPATH=$lue_install_prefix/lib64/python3.9
export LD_PRELOAD=$EBROOTGPERFTOOLS/lib/libtcmalloc_minimal.so.4


function run_on_snellius_node()
{
    nr_numa_nodes=$1

    nr_cluster_nodes=1
    nr_cpus_per_task=16
    nr_localities=$(expr $nr_cluster_nodes \* $nr_numa_nodes)

    # # Start a cooperating set of processes:
    python /sw/arch/Centos8/EB_production/2021/software/HPX/1.7.1-foss-2021a/bin/hpxrun.py \
        --parcelport=mpi \
        --runwrapper=mpi \
        --localities=$nr_localities \
        --thread=$nr_cpus_per_task \
        --verbose \
        `which python` -- \
            /home/jaarsveldb/lue_split/model.py

}

# Pick one of these to try things out:
# run_on_snellius_node 1  # NUMA nodes → 16 CPU cores
# run_on_snellius_node 3  # NUMA nodes → 16 CPU cores
# run_on_snellius_node 5  # NUMA nodes → 16 CPU cores
run_on_snellius_node 7  # NUMA nodes → 16 CPU coress