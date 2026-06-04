import json
from datetime import datetime

def save_research_result(
    path,
    hypothesis,
    metrics,
    conclusion
):

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "hypothesis": hypothesis,
        "metrics": metrics,
        "conclusion": conclusion
    }

    with open(
        f"{path}/research.json",
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )
