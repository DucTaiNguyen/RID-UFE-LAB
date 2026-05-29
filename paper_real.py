def generate_latex(m):

    tex = f"""
\\documentclass[10pt]{{article}}

\\title{{RID-UFE Real Data Scientific Report}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
This paper analyzes real-world Bitcoin market data
using a recursive information dynamics framework.
\\end{{abstract}}

\\section{{Data}}

Bitcoin Price (USD): {m['price']}

\\section{{Method}}

We define:

Signal = price / 100000

Noise = price mod 1000

Score = Signal - Noise

\\section{{Results}}

Score: {m['score']}

\\section{{Discussion}}

The system demonstrates how financial markets
can be interpreted as information fields.

\\end{{document}}
"""

    with open("paper/main.tex", "w") as f:
        f.write(tex)

    return "paper/main.tex"
