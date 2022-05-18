# Snellius

## Build LUE
LUE depends on various 3rd party software. For general information about building LUE, see the
[Installation page](https://lue.computationalgeography.org/doc/install/index.html). Here,
we only describe how to build LUE on snellius.

These are the steps when starting from scratch:
1. Setup environment for building LUE
1. Clone LUE repository
1. Configure build and generate build scripts
1. Build LUE
1. Install LUE

Building software on a login node of snellius is a bad idea. It will take forever (hours). It
is better to use a cluster node for that. Then a build will take minutes instead. This is one
way to do it:

```bash
# Request cluster resources for half an hour and wait for them to become allocated
salloc -n 1 -c 32 -t 0:30:00

# Obtain the hostname to ssh into
squeue
```

Login to the node assigned to you and then perform the next steps.


### Setup environment
Install CMake >= 3.22. KDJ requested a module for this but it is not yet available.

```bash
cd $HOME/tmp
wget https://github.com/Kitware/CMake/releases/download/v3.23.1/cmake-3.23.1-linux-x86_64.tar.gz

# For example
mkdir $HOME/opt
cd $HOME/opt
tar zxf $HOME/tmp/cmake-3.23.1-linux-x86_64.tar.gz
ln -s cmake-3.23.1-linux-x86_64 cmake
echo 'export PATH="$HOME/opt/cmake/bin:$PATH"' >> $HOME/.bash_profile
```

Start a new shell and verify CMake is found:

```bash
# Should print the version just installed
cmake --version
```

Load required EasyBuild modules:

```bash
module load 2021 \
    GDAL/3.3.0-foss-2021a \
    Miniconda3/4.9.2 \
    Ninja/1.10.2-GCCcore-10.3.0 \
    HPX/1.7.1-foss-2021a
```

Setup a Conda environment with additional packages required for building LUE (Conan, NumPy). Name
it however you like. Add any other packages you need for your project. Tip: store this information
in a YAML file for later reuse. See Conda docs.

```bash
conda create --name lue --channel conda-forge python=3.9 conan numpy
conda init bash  # Only needed the first time you use Conda
```

Start a new shell and activate the Conda environment:

```bash
conda activate lue
```

Update the Conan profile used when Conan needs to locally build packages.

```bash
# Only needed the first time you use Conan
conan profile update settings.compiler.libcxx=libstdc++11 default
```


### Clone repository
Determine where the LUE sources, generated binary files, and installed runtime
files must be stored. Here, we use `$HOME/development/project/computational_geography/lue`,
`$HOME/tmp/lue`, and `$HOME/opt/lue` for these, respectively. Pick whatever you
want.


```bash
git clone https://github.com/computationalgeography/lue.git \
    $HOME/development/project/computational_geography/lue

# ATM the LUE sources we need are in a separate branch
git checkout gh420
```

Before continuing, verify on [this page](https://github.com/computationalgeography/lue) whether
the Linux CI build succeeded: switch to the right branch if you are not using the master
branch, and scroll to the CI builds section. If the Linux CI icon is not green, talk to Kor before
continuing.


### Configure build
Use CMake to configure the LUE build and generate build scripts that can be used to build and
install LUE.

```bash
cmake -G Ninja \
    -S $HOME/development/project/computational_geography/lue \
    -B $HOME/tmp/lue \
    -D CMAKE_BUILD_TYPE=Release \
    -D LUE_BUILD_DATA_MODEL=TRUE \
    -D LUE_DATA_MODEL_WITH_PYTHON_API=TRUE \
    -D LUE_DATA_MODEL_WITH_UTILITIES=TRUE \
    -D LUE_BUILD_FRAMEWORK=TRUE \
    -D LUE_FRAMEWORK_WITH_PYTHON_API=TRUE \
    -D LUE_HAVE_FMT=FALSE \
    -D LUE_HAVE_DOCOPT=FALSE
```

### Build and install
Use CMake to build and install the LUE targets we asked for.

```bash
cd $HOME/tmp/lue
cmake --build . --target all --parallel 32
cmake --install . --component lue_runtime --prefix $HOME/opt/lue
```

This should result in a LUE installation in `$HOME/opt/lue`.

```bash
tree $HOME/opt/lue
```

The command line utilities are stored in `bin` and the Python package is stored in
`lib64/python3.9`.


## Use LUE
To be able to use LUE, expand two environment variables. Either add them to your `.bash_profile`
or to some other custom shell script you source when working with LUE.

```bash
echo 'export PATH="$HOME/opt/lue/bin:$PATH"' >> $HOME/.bash_profile
echo 'export PYTHONPATH="$HOME/opt/lue/lib64/python3.9:$PYTHONPATH"' >> $HOME/.bash_profile
```

These commands should now run successfully:

```bash
lue_validate --version
python -c "import lue; print(lue.__version__)"
```

If not, then check these:
- Python interpreter you currently use is the same one used when building LUE. Check this with:
  ```bash
  python --version
  ```
  The main and major version numbers must match.
- The paths added to `PATH` and `PYTHONPATH` point to existing paths.

Exit the node again and release the resources.

```bash
# Note JOBID
squeue
scancel <jobid>
```


## Update LUE
TODO


