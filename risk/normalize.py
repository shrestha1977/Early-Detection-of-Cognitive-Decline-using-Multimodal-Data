import pickle
import os

stats_file = os.path.join(
    os.path.dirname(__file__),
    "statistics.pkl"
)

with open(stats_file, "rb") as f:
    stats = pickle.load(f)


def z_score(value, mean, std):

    if std == 0:
        return 0

    return (value - mean) / std


def normalize_math(num_ability_score):

    return z_score(
        num_ability_score,
        stats["math_mean"],
        stats["math_std"]
    )


def normalize_stroop(
    Stroop_error,
    stroop_mean_RT,
    Stroop_interference
):

    # Lower error is better
    error_z = -z_score(
        Stroop_error,
        stats["Stroop_error_mean"],
        stats["Stroop_error_std"]
    )

    # Lower reaction time is better
    rt_z = -z_score(
        stroop_mean_RT,
        stats["stroop_mean_RT_mean"],
        stats["stroop_mean_RT_std"]
    )

    # Lower interference is better
    interference_z = -z_score(
        Stroop_interference,
        stats["Stroop_interference_mean"],
        stats["Stroop_interference_std"]
    )

    return (
        error_z +
        rt_z +
        interference_z
    ) / 3


def normalize_mrt(
    MR_acc,
    MR_reaction,
    MR_spatial_score,
    MR_high_angle_accuracy
):

    # Higher accuracy is better
    acc_z = z_score(
        MR_acc,
        stats["MR_acc_mean"],
        stats["MR_acc_std"]
    )

    # Lower reaction time is better
    reaction_z = -z_score(
        MR_reaction,
        stats["MR_reaction_mean"],
        stats["MR_reaction_std"]
    )

    # Higher spatial score is better
    spatial_z = z_score(
        MR_spatial_score,
        stats["MR_spatial_score_mean"],
        stats["MR_spatial_score_std"]
    )

    # Higher high-angle accuracy is better
    high_angle_z = z_score(
        MR_high_angle_accuracy,
        stats["MR_high_angle_accuracy_mean"],
        stats["MR_high_angle_accuracy_std"]
    )

    return (
        acc_z +
        reaction_z +
        spatial_z +
        high_angle_z
    ) / 4
