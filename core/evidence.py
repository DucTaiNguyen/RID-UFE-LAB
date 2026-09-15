import json
import os


def classify_evidence(
    observed_association,
    null_p_value,
    train_association,
    test_association,
    stability_threshold=0.10,
):
    """
    Evidence classification for temporal association.

    Important:
    - Statistical association is not causality.
    - In-sample significance is not sufficient for prediction.
    - Out-of-sample sign/magnitude stability is required
      for a predictive claim to advance.
    """

    same_sign = (
        train_association == 0
        or test_association == 0
        or (train_association > 0) == (test_association > 0)
    )

    magnitude_ratio = (
        abs(test_association)
        / (abs(train_association) + 1e-12)
    )

    stable_magnitude = (
        stability_threshold
        <= magnitude_ratio
        <= 1.0 / stability_threshold
    )

    time_series_null_supported = bool(
        null_p_value < 0.05
    )

    out_of_sample_stable = bool(
        same_sign and stable_magnitude
    )

    if (
        time_series_null_supported
        and out_of_sample_stable
    ):
        predictive_claim = (
            "SUPPORTED_FOR_FURTHER_TESTING"
        )
    else:
        predictive_claim = (
            "NOT_ESTABLISHED"
        )

    return {
        "observed_association":
            float(observed_association),

        "time_series_null_supported":
            time_series_null_supported,

        "out_of_sample_stable":
            out_of_sample_stable,

        "predictive_claim":
            predictive_claim,

        "causal_claim":
            "NOT_ESTABLISHED",
    }


def evidence_status(evidence):
    """
    Distinguish execution status from scientific claim status.
    """

    required = [
        "observed_association",
        "null_p_value_two_sided",
        "train_association",
        "test_association",
        "predictive_claim",
        "causal_claim",
    ]

    complete = all(
        key in evidence
        for key in required
    )

    if not complete:
        return "VALIDATION_INCOMPLETE"

    return "VALIDATION_COMPLETE"


def save_evidence(path, evidence):
    os.makedirs(path, exist_ok=True)

    evidence = dict(evidence)

    evidence["status"] = evidence_status(
        evidence
    )

    output = os.path.join(
        path,
        "evidence.json"
    )

    with open(
        output,
        "w"
    ) as f:
        json.dump(
            evidence,
            f,
            indent=4
        )

    return output
