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
    print_diff_size_details(aligned_file_merges)
    histogram(
        aligned_file_merges,
        bins=bins,
        xlabel="Line diff size",
    )


def print_diff_size_details(diff_sizes: pd.DataFrame) -> None:
    print(f"Amount of file merges considered:\n\t{len(diff_sizes)}")

    print("Median diff sizes per tool")
    print_tool_results(diff_sizes, callback=np.median)

    print("Max diff sizes per tool")
    print_tool_results(diff_sizes, callback=np.max)

    print_size_compared_to_spork(diff_sizes)


def plot_runtimes():
    running_times = pd.read_csv(THIS_DIR / "results" / "running_times.csv")
    bins = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
    median_running_times = compute_median_running_times(running_times)
    print_running_time_details(median_running_times)
    histogram(
        median_running_times,
        bins=bins,
        xlabel="Median running time of 10 executions (seconds)",
    )


def print_running_time_details(running_times: pd.DataFrame) -> None:
    print(f"Amount of merge scenarios where all tools succeed:\n\t{len(running_times)}")

    print("Sum of medians per tool:")
    print_tool_results(running_times, callback=np.sum)

    print("Median of running times per tool:")
    print_tool_results(running_times, callback=np.median)

    print("Max running times per tool:")
    print_tool_results(running_times, callback=np.max)

    print(f"Amount of timeouts per tool:")
    for tool in TOOLS:
        num_timeouts = len(
            FILE_MERGE_EVALS.query(f"merge_cmd == '{tool}' and outcome == 'timeout'")
        )
        print(f"\t{tool.upper()}: {num_timeouts}")

    print("Amount of running times per tool < .5 seconds")
    print_tool_results(running_times, callback=count(lambda x: x < 0.5))

    print("Amount of running times per tool >= 4 seconds")
    print_tool_results(running_times, callback=count(lambda x: x >= 4))

    print_size_compared_to_spork(running_times)


def plot_conflict_sizes():
    # note: using [-3, 1) as the first bin is a hack to ensure that all bins
    # are of equal size, graphically
    left_bound = -3
    bins = [left_bound, 1, 5, 9, 13, 17, 21, 25, 29, 33]
    non_fail_conflict_dirs = CONFLICT_MERGE_DIRS - FAIL_MERGE_DIRS
    aligned_conflict_sizes = (
        FILE_MERGE_EVALS[FILE_MERGE_EVALS.merge_dir.isin(non_fail_conflict_dirs)]
        .groupby(["merge_dir", "merge_cmd"])
        .conflict_size.sum()
        .unstack()
    )
    print_conflict_size_details(aligned_conflict_sizes)
    histogram(
        aligned_conflict_sizes,
        bins=bins,
        xlabel="Conflict size per file merge",
        bound_to_label={left_bound: "0"},
    )


def print_conflict_size_details(conflict_sizes: pd.DataFrame) -> None:
    print(f"Amount of file merges considered:\n\t{len(conflict_sizes)}")

    print("Max conflict sizes per tool:")
    print_tool_results(conflict_sizes, callback=np.max)

    print("Median conflict sizes per tool:")
    print_tool_results(conflict_sizes, callback=np.median)

    print("Total conflict sizes per tool:")
    print_tool_results(conflict_sizes, callback=np.sum)

    print("Amount of files with >= 5 conflicting lines")
    print_tool_results(conflict_sizes, callback=count(lambda size: size >= 5))

    print("Amount of files with >= 10 conflicting lines")
    print_tool_results(conflict_sizes, callback=count(lambda size: size >= 10))

    print("Amount of files with >= 20 conflicting lines")
    print_tool_results(conflict_sizes, callback=count(lambda size: size >= 20))

    print_size_compared_to_spork(conflict_sizes)


def plot_conflict_hunk_quantities():
    bins = [0, 1, 2, 3, 4, 5]
    non_fail_conflict_dirs = CONFLICT_MERGE_DIRS - FAIL_MERGE_DIRS
    aligned_conflicts = (
        FILE_MERGE_EVALS[FILE_MERGE_EVALS.merge_dir.isin(non_fail_conflict_dirs)]
        .groupby(["merge_dir", "merge_cmd"])
        .num_conflicts.sum()
        .unstack()
    )
    print_conflict_quantity_details(aligned_conflicts)
    histogram(
        aligned_conflicts,
        bins=bins,
        xlabel="Amount of conflict hunks per file merge",
    )


def print_conflict_quantity_details(conflicts: pd.DataFrame) -> None:
    print(
        f"Amount of file merges with at least one conflict from one tool:\n\t{len(conflicts)}"
    )

    print(f"Amount of files with conflicts per tool:")
    print_tool_results(conflicts, callback=np.count_nonzero)

    print(f"Total amount of conflict hunks per tool:")
    print_tool_results(conflicts, callback=np.sum)

    print_size_compared_to_spork(conflicts)


def print_size_compared_to_spork(frame: pd.DataFrame) -> None:
    print("Amount of cases where where SPORK's results are lesser, equal, greater:")

    def compute_comparison(cmp: str) -> str:
        amount = len(frame.query(cmp))
        return f"\t{cmp}: {amount}"

    for tool in filter(lambda t: t != "spork", TOOLS):
        print(compute_comparison(f"spork < {tool}"))
        print(compute_comparison(f"spork == {tool}"))
        print(compute_comparison(f"spork > {tool}"))


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
    print_diff_size_details(aligned_file_merges)
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


def histogram(data, bins, xlabel, ylabel="Frequency", bound_to_label=None):
    bound_to_label = bound_to_label or {}
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
        if bin_value in bound_to_label:
            return bound_to_label[bin_value]
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

    print(pg.wilcoxon(spork_values, jdime_values, alternative="two-sided"))
    print(pg.wilcoxon(spork_values, automergeptm_values, alternative="two-sided"))

    plt.show()


def set_hatches(ax):
    for patch in ax.patches[len(ax.patches) // 3 :]:
        patch.set_hatch("/")
    for patch in ax.patches[int(2 / 3 * len(ax.patches)) :]:
        patch.set_hatch("x")


def compute_median_running_times(running_times: pd.DataFrame) -> pd.DataFrame:
    return (
        running_times.groupby(["merge_dir", "merge_cmd"])["running_time"]
        .median()
        .unstack()
    )


def count(predicate):
    def _count(data):
        return sum(int(predicate(v)) for v in data if predicate(v))

    return _count


def print_tool_results(data: pd.DataFrame, callback) -> None:
    results = {}
    for tool in TOOLS:
        results[tool] = callback(getattr(data, tool))
        print(f"\t{tool.upper()}: {results[tool]}")

    for tool in filter(lambda t: t != "spork", TOOLS):
        spork_result = results["spork"]
        other_result = results[tool]
        diff = other_result - spork_result
        reduction = 100 * (other_result - spork_result) / other_result
        print(
            f"\tSPORK reduction vs {tool.upper()}: absolute={diff}, percentage={reduction:.2f}%"
        )


if __name__ == "__main__":
    plot_conflict_hunk_quantities()
    plot_conflict_sizes()
    plot_runtimes()
    plot_git_diff_sizes()
    plot_char_diff_size()
    plot_char_diff_ratio()
