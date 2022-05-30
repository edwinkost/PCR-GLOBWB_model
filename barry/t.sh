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
{
    nr_numa_nodes=$1

    # We want a process per NUMA node:
    # - ntasks: $nr_numa_nodes
    # - cpus-per-task: 16

    nr_cluster_nodes=1
    nr_cpus_per_task=16
    nr_localities=$(expr $nr_cluster_nodes \* $nr_numa_nodes)

#~     # Start a cooperating set of processes:
#~     python /sw/arch/Centos8/EB_production/2021/software/HPX/1.7.1-foss-2021a/bin/hpxrun.py \
#~         --parcelport=mpi \
#~         --runwrapper=mpi \
#~         --localities=$nr_localities \
#~         --thread=$nr_cpus_per_task \
#~         --verbose \
#~         `which python` -- \
#~             /home/edwin/github/edwinkost/PCR-GLOBWB_model/example_lue/example_from_kor/hello_lue.py \
#~                 6000,4000 1000,1000 \
#~                 --hpx:print-bind

#~     # Start a cooperating set of processes:
#~     python /home/edwin/github/edwinkost/PCR-GLOBWB_model/example_lue/example_from_kor/hello_lue.py \
#~                 6000,4000 1000,1000 \
#~                 --hpx:print-bind

    # Start a cooperating set of processes:
    python /home/jaarsveldb/lue/PCR-GLOBWB_model/barry/hamonETPfunctions_lue.py \
                # 6000,4000 1000,1000 \
                # --hpx:print-bind

}

#
function run_on_snellius_partition()
{
    nr_cluster_nodes=$1

    # We want a process per NUMA node:
    # - ntasks: $nr_cluster_nodes x $nr_numa_nodes
    # - cpus-per-task: 16

    nr_numa_nodes_per_node=8
    nr_cpus_per_task=16
    nr_localities=$(expr $nr_cluster_nodes \* $nr_numa_nodes_per_node)

    # Allocate resources and start a cooperating set of processes:
    salloc \
        --nodes=$nr_cluster_nodes \
        --ntasks=$nr_localities \
        --cpus-per-task=$nr_cpus_per_task \
        srun \
            python \
                $LUE/hello_lue.py \
                    60000,40000 1000,1000 \
                    --hpx:print-bind
}


# Pick one of these to try things out:
run_on_snellius_node 2  # NUMA nodes → 32 CPU cores
# run_on_snellius_partition 2  # Cluster nodes → 256 CPU cores
