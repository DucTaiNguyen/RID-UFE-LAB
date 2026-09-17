from dataclasses import dataclass


@dataclass(frozen=True)
class ClaimDecision:
    statistical_status: str
    robustness_status: str
    predictive_status: str
    causal_status: str
    reasons: tuple[str, ...]


def evaluate_claims(
    *,
    p_value=None,
    effect_size=None,
    out_of_sample_stable=False,
    null_supported=False,
    causal_design=False,
):
    reasons = []

    # Statistical evidence
    if p_value is None:
        statistical_status = "NOT_ESTABLISHED"
        reasons.append("No p-value available.")
    elif p_value < 0.05:
        statistical_status = "SUPPORTED"
        reasons.append("Association passes the nominal statistical threshold.")
    else:
        statistical_status = "NOT_ESTABLISHED"
        reasons.append("Association does not pass the nominal statistical threshold.")

    # Robustness
    if null_supported:
        robustness_status = "SUPPORTED"
    else:
        robustness_status = "NOT_ESTABLISHED"
        reasons.append("Robustness against the selected null model is not established.")

    # Predictive claim
    if (
        statistical_status == "SUPPORTED"
        and robustness_status == "SUPPORTED"
        and out_of_sample_stable
    ):
        predictive_status = "SUPPORTED_FOR_FURTHER_TESTING"
    else:
        predictive_status = "NOT_ESTABLISHED"
        reasons.append(
            "Out-of-sample predictive stability is not established."
        )

    # Causal claim
    if causal_design and predictive_status == "SUPPORTED_FOR_FURTHER_TESTING":
        causal_status = "SUPPORTED_FOR_FURTHER_TESTING"
    else:
        causal_status = "NOT_ESTABLISHED"
        reasons.append(
            "No causal identification design is established."
        )

    return ClaimDecision(
        statistical_status=statistical_status,
        robustness_status=robustness_status,
        predictive_status=predictive_status,
        causal_status=causal_status,
        reasons=tuple(reasons),
    )
