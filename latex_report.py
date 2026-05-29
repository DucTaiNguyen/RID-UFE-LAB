def generate_latex(data):

    tex = f"""
\\documentclass{{article}}
\\usepackage{{amsmath}}

\\title{{RID-UFE AI Research Report}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\section{{Results}}

\\textbf{{Score}}: {data['score']} \\\\
\\textbf{{Hypothesis}}: {data['hypothesis']}

\\section{{Interpretation}}

The system processes real-world signals and generates adaptive hypotheses.

\\end{{document}}
"""

    with open("report.tex", "w") as f:
        f.write(tex)

    return "report.tex"
