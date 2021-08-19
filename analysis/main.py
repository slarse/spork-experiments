import pathlib
import math
import itertools
import pandas as pd
import scipy.stats
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pingouin as pg

THIS_DIR = pathlib.Path(__file__).parent

sns.set(font_scale=3, palette="pastel", style="ticks", context="paper")

FILE_MERGE_EVALS = pd.read_csv(THIS_DIR / "results" / "file_merge_evaluations.csv")
TOOLS = ["spork", "jdime", "automergeptm"]

# merge directories in which JDime or Spork (or both) exhibit fails/conflicts
FAIL_MERGE_DIRS = set(
    FILE_MERGE_EVALS.query(
        "outcome == 'fail' or outcome == 'timeout'"
    ).merge_dir.unique()
)
CONFLICT_MERGE_DIRS = set(
    FILE_MERGE_EVALS.query("outcome == 'conflict'").merge_dir.unique()
)


def plot_git_diff_sizes():
    filtered_file_merges = FILE_MERGE_EVALS[
        ~FILE_MERGE_EVALS.merge_dir.isin(FAIL_MERGE_DIRS | CONFLICT_MERGE_DIRS)
    ]
    aligned_file_merges = (
        filtered_file_merges.groupby(["merge_dir", "merge_cmd"])
        .line_diff_size.sum()
        .unstack()
    )
    bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650]
    histogram(
        aligned_file_merges,
        bins=bins,
        xlabel="GitDiff size (insertions + deletions)",
    )


def plot_runtimes():
    running_times = pd.read_csv(THIS_DIR / "results" / "running_times.csv")
    bins = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
    median_running_times = compute_median_running_times(running_times)
    histogram(
        median_running_times,
        bins=bins,
        xlabel="Median running time of 10 executions (seconds)",
    )


def plot_mean_conflict_sizes():
    bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    aligned_mean_conflict_sizes = get_aligned_mean_conflict_sizes().query(
        "spork > 0 or jdime > 0 or automergeptm > 0"
    )
    histogram(
        aligned_mean_conflict_sizes,
        bins=bins,
        xlabel="Mean conflict hunk size per file",
    )


def plot_conflict_hunk_quantities():
    bins = [0, 1, 2, 3, 4, 5]
    non_fail_conflict_dirs = CONFLICT_MERGE_DIRS - FAIL_MERGE_DIRS
    aligned_conflicts = (
        FILE_MERGE_EVALS[FILE_MERGE_EVALS.merge_dir.isin(non_fail_conflict_dirs)]
        .groupby(["merge_dir", "merge_cmd"])
        .num_conflicts.sum()
        .unstack()
    )
    histogram(
        aligned_conflicts,
        bins=bins,
        xlabel="Amount of conflict hunks per file",
    )


def plot_char_diff_size():
    bins = [0, 1000, 2000, 3000, 4000, 5000, 6000]
    filtered_file_merges = FILE_MERGE_EVALS[
        ~FILE_MERGE_EVALS.merge_dir.isin(FAIL_MERGE_DIRS | CONFLICT_MERGE_DIRS)
    ]
    aligned_file_merges = (
        filtered_file_merges.groupby(["merge_dir", "merge_cmd"])
        .char_diff_size.sum()
        .unstack()
    )
    histogram(
        aligned_file_merges,
        bins=bins,
        xlabel="Character diff size",
    )


def plot_char_diff_ratio():
    bins = [0.75, 0.8, 0.85, 0.9, 0.95, 1]
    filtered_file_merges = FILE_MERGE_EVALS[
        ~FILE_MERGE_EVALS.merge_dir.isin(FAIL_MERGE_DIRS | CONFLICT_MERGE_DIRS)
    ]
    aligned_file_merges = (
        filtered_file_merges.groupby(["merge_dir", "merge_cmd"])
        .char_diff_ratio.sum()
        .unstack()
    )
    histogram(
        aligned_file_merges,
        bins=bins,
        xlabel="Character diff ratio",
    )


def histogram(data, bins, xlabel, ylabel="Frequency"):
    spork_values = data.spork
    jdime_values = data.jdime
    automergeptm_values = data.automergeptm

    smallest_value = min(
        0, min(itertools.chain(spork_values, jdime_values, automergeptm_values))
    )
    largest_value = max(
        itertools.chain(spork_values, jdime_values, automergeptm_values)
    )

    has_lower_bound = smallest_value >= bins[0]
    has_upper_bound = largest_value < bins[-1]

    def get_ticklabel(bin_value):
        if bin_value == bins[0] and not has_lower_bound:
            return str(int(math.floor(smallest_value)))
        elif bin_value == bins[-1] and not has_upper_bound:
            # bins are exclusive to the right, so max bin must be 1 larger
            max_bin = int(math.ceil(largest_value + 1))
            return str(max_bin)
        else:
            return str(bin_value)

    # limits values to be in the range of bins, but does not remove any values
    clipped_spork_values = np.clip(spork_values, bins[0], bins[-1])
    clipped_jdime_values = np.clip(jdime_values, bins[0], bins[-1])
    clipped_automergeptm_values = np.clip(automergeptm_values, bins[0], bins[-1])

    _, ax = plt.subplots()
    plt.hist(
        [clipped_spork_values, clipped_jdime_values, clipped_automergeptm_values],
        bins=bins,
    )
    set_hatches(ax)

    handles = [ax.patches[0], ax.patches[len(ax.patches) // 2], ax.patches[-1]]
    labels = ["Spork", "JDime", "AutoMergePTM"]
    plt.legend(handles, labels)
    plt.xticks(bins)
    plt.tick_params(axis="both", which="major", labelsize=20)

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    ticklabels = list(map(get_ticklabel, bins))
    ax.set_xticklabels(ticklabels)

    friedman = scipy.stats.friedmanchisquare(
        spork_values, jdime_values, automergeptm_values
    )
    print(f"Friedman Chi Squared p-value: {friedman.pvalue}")

    print(spork_values.describe())
    print(jdime_values.describe())
    print(automergeptm_values.describe())
    print(pg.wilcoxon(spork_values, jdime_values, alternative="two-sided"))
    print(pg.wilcoxon(spork_values, automergeptm_values, alternative="two-sided"))

    plt.show()


def set_hatches(ax):
    for patch in ax.patches[len(ax.patches) // 3 :]:
        patch.set_hatch("/")
    for patch in ax.patches[int(2 / 3 * len(ax.patches)) :]:
        patch.set_hatch("x")


def get_aligned_mean_conflict_sizes():
    non_fail_conflict_dirs = CONFLICT_MERGE_DIRS - FAIL_MERGE_DIRS
    non_fail_conflict_merges = FILE_MERGE_EVALS[
        FILE_MERGE_EVALS.merge_dir.isin(non_fail_conflict_dirs)
    ]
    return (
        non_fail_conflict_merges.groupby(["merge_dir", "merge_cmd"])[
            ["num_conflicts", "conflict_size"]
        ]
        .apply(avg_chunk_size)
        .unstack()
    )


def avg_chunk_size(row):
    return int(row.conflict_size) / max(1, int(row.num_conflicts))


def compute_median_running_times(running_times: pd.DataFrame) -> pd.DataFrame:
    return (
        running_times.groupby(["merge_dir", "merge_cmd"])["running_time"]
        .median()
        .unstack()
    )


if __name__ == "__main__":
    plot_conflict_hunk_quantities()
    plot_mean_conflict_sizes()
    plot_runtimes()
    plot_git_diff_sizes()
    plot_char_diff_size()
    plot_char_diff_ratio()
