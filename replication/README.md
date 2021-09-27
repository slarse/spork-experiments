# Reproduction of Spork experiments
This directory contains scripts and instructions for reproducing the
experiments conducted with Spork.

## Directory overview
The following results files are available in this directory:

* [candidate_projects.txt](candidate_projects.txt)
    - A list of candidate projects that fit the selection criteria.
* [buildable_candidates.txt](buildable_candidates.txt)
    - A filtered list of the candidate projects that were also buildable on the
      experiment system.
* [projects.csv](projects.csv)
    - A table of projects used in the evaluation.
* [file_merge_evaluations.csv](file_merge_evaluations.csv)
    - Results evaluating the file merges.
* [running_times.csv](running_times.csv)
    - Running time measurements, executed 10 times for each file merge and
      merge tool.

For more detailed results, including the actual file merges computed by each
tool, you must download the replication package as described below.

## Setting up for the experiments
The [install.sh](install.sh) script is designed to setup the experiments on
Ubuntu 18.04. It will both fetch all required resources (including the
replication package), install required software, as well as configure Git and
other related software correctly. It may work with other Debian-based
distributions, but we have only tested it on Ubuntu 18.04. [Download Ubuntu
18.04 from here](https://releases.ubuntu.com/18.04.4/).

> **Important:** The install script will both install and remove packages, and
> so we do not recommend running it on a machine that is used for other things.
> We recommend using a dedicated install for this experiment, or a virtual
> machine such as VirtualBox.

> **Note:** If you just want to look at the detailed results, then you don't
> need to run the install script. Instead, refer to [Getting the replication
> package](#getting-the-replication-package).

The final output of the install script should tell you to source a file before
running the experiments. This file will set some environment variables and
activate a Python virtual environment in which the benchmark package is
installed. So run `source` on the file.

You should also have a directory called `replication_package` in your current
working directory. In order to replicate the experiments, go to
`replication_package/replication/replication_experiment` and run the
`run_experiments.py` file.

```bash
cd replication_package/replication/replication_experiment
python run_experiments.py
```

Again, don't forget to source the environment file first, or the experiments
will surely fail to run. We give a brief overview of the replication package in
[Replication package overview](#replication-package-overview), which may prove
helpful if you run into issues.

## Getting the replication package
You can download the replication package manually [from
here](https://github.com/KTH/spork/releases/download/v0.5.1/replication_package.tar.gz),
or simply run the following shell command:

```bash
curl https://github.com/KTH/spork/releases/download/v0.5.1/replication_package.tar.gz \
    -o replication_package.tar.gz
```

Then, unpack the replication package like so.

```bash
tar -xzf replication_package.tar.gz
```

This will leave you with a directory called `replication_package`, containing
all resources.

> **Important:** If you wish to actually run the experiments, use the install
> script as described in [Setting
> up for the experiments](#setting-up-for-the-experiments) instead.

## Replication package overview
There are two important directories in the replication package: `results` and
`replication`. In the `results` directory, you will find the results from the
experiments, such as merged source files and all input files. In the
`replication` directory, you will find the means of reproducing the
experiments.

### Software
In `replication/software`, you will find additional software required for
running the experiments (except for `JDime` and `AutomergePTM`, which we clone
on-demand).

All of the jar files have associated shell scripts in
`replication/software/executables`, that just wrap the jar-files to make them
easier to execute during the benchmarks. These wrappers require that the
`EXPERIMENT_SOFTWARE_ROOT` variable is the absolute path to
`replication/software` (the `install.sh` script takes care of this) to work
correctly.

The actual benchmark script is located in `replication/software/benchmark`, and
is a Python package that can be installed with `pip`. If you use the
`install.sh` script, the benchmark package will already be installed, and you
can access its CLI by running:

```bash
python3 -m benchmark.cli -h
```

> **Important:** The benchmark package requires that the wrappers in
> `replication/software/executables` are on the `PATH`, and that
> `EXPERIMENT_SOFTWARE_ROOT` is correctly set!
