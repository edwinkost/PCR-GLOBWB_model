#!/usr/bin/env python
import lue.framework as lfr
import docopt
import numpy as np
import os.path
import sys


# LUE demo script, for showing how to use LUE:
# - Import of package
# - Start / stop runtime
# - Array size, partition size


@lfr.runtime_scope
def hello_lue(
        array_shape,
        partition_shape):

    # The HPX runtime is started on all localities. This function is only called on the root
    # locality.

    # Create an array, initialized with a constant value
    array = lfr.create_array(
        array_shape=array_shape, partition_shape=partition_shape,
        dtype=np.dtype(np.float32), fill_value=5.5)

    # Perform some computations
    cell = (lfr.uniform(array, 0, 10) * array) / array

    # The HPX runtime will be stopped automatically on all localities once the computations
    # are done.


usage = """\
Demonstrate how use LUE

Usage:
    {command} <array> <partition>

Options:
    array           Shape of array: nr_rows,nrcols
    partition       Shape of partition: nr_rows,nrcols
    -h --help       Show this screen
""".format(
    command = os.path.basename(sys.argv[0]))


def parse_tuple(string):

    return tuple([token.strip() for token in string.split(",")])


def parse_shape(string):

    return tuple([int(element) for element in parse_tuple(string)])


if __name__ == "__main__":
    # Filter out arguments meant for the HPX runtime
    argv = [arg for arg in sys.argv[1:] if not arg.startswith("--hpx")]
    arguments = docopt.docopt(usage, argv)

    array_shape = parse_shape(arguments["<array>"])
    partition_shape = parse_shape(arguments["<partition>"])

    hello_lue(array_shape, partition_shape)
