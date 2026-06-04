def generate_report(
    exp_id,
    metrics,
    output_file
):

    report = f"""
# RID-UFE Information Field Report

## Experiment

{exp_id}

## Results

Volatility: {metrics["volatility"]}

Entropy: {metrics["entropy"]}

Spectral Gap: {metrics["spectral_gap"]}

## Discussion

This experiment analyzes Bitcoin as an information field using graph spectral methods.

Higher entropy indicates greater uncertainty.

Spectral gap characterizes graph connectivity structure.
"""

    with open(
        output_file,
        "w"
    ) as f:

        f.write(report)
