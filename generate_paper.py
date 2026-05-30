with open("results.txt", "r") as f:
    results = f.read()

latex = r"""
\documentclass{article}

\title{RID-UFE Bitcoin Research}
\author{Tai D. Nguyen}
\date{}

\begin{document}

\maketitle

\section{Abstract}

This report analyzes Bitcoin market information.

\section{Results}

\begin{verbatim}
""" + results + r"""
\end{verbatim}

\section{Conclusion}

This is the first data-driven RID-UFE report.

\end{document}
"""

with open("paper/main.tex", "w") as f:
    f.write(latex)

print("Generated: paper/main.tex")
