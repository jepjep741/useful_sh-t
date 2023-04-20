import os
import json
import csv
import subprocess
import sys

# Functions for converting reports to LaTeX format
# For Wapiti
def convert_wapiti_vuln_to_latex(vuln):
    latex_vuln = f"\\textbf{{Name}}: {vuln['name']}\\\\\n"
    latex_vuln += f"\\textbf{{Description}}: {vuln['description']}\\\\\n"
    latex_vuln += f"\\textbf{{URL}}: \\url{{{vuln['url']}}}\\\\\n"
    latex_vuln += f"\\textbf{{Severity}}: {vuln['severity']}\\\\\n"
    latex_vuln += "\\vspace{1em}\n"
    return latex_vuln


# For Nikto2
def convert_nikto_vuln_to_latex(vuln):
    latex_vuln = f"\\textbf{{IP}}: {vuln['IP']}\\\\\n"
    latex_vuln += f"\\textbf{{Hostname}}: {vuln['hostname']}\\\\\n"
    latex_vuln += f"\\textbf{{Port}}: {vuln['port']}\\\\\n"
    latex_vuln += f"\\textbf{{URI}}: \\url{{{vuln['uri']}}}\\\\\n"
    latex_vuln += f"\\textbf{{Description}}: {vuln['description']}\\\\\n"
    latex_vuln += "\\vspace{1em}\n"
    return latex_vuln

# For SQLMap
def convert_sqlmap_vuln_to_latex(vuln):
    latex_vuln = f"\\textbf{{Parameter}}: {vuln['parameter']}\\\\\n"
    latex_vuln += f"\\textbf{{Injection Type}}: {vuln['injection_type']}\\\\\n"
    latex_vuln += f"\\textbf{{Technique}}: {vuln['technique']}\\\\\n"
    latex_vuln += f"\\textbf{{DBMS}}: {vuln['dbms']}\\\\\n"
    latex_vuln += "\\vspace{1em}\n"
    return latex_vuln

# Main function to run scans, convert reports, and compile the LaTeX document
def main():
    target_url = sys.argv[1]

    # Run Wapiti scan
    subprocess.run(['wapiti', '-u', target_url, '-f', 'json', '-o', 'wapiti_report.json'])

    # Run Nikto2 scan
    subprocess.run(['nikto', '-h', target_url, '-o', 'nikto_report.csv', '-Format', 'csv'])

    # Run SQLMap scan
    subprocess.run(['python', 'sqlmap.py', '-u', target_url, '--batch', '--output-dir=output', '--forms', '--threads=10', '--eta', '--flush-session', '--fresh-queries', '--smart', '--level=3', '--risk=3', '--random-agent', '--json-output'])

    # Convert Wapiti JSON report to LaTeX
    with open('wapiti_report.json', 'r') as f:
        wapiti_report = json.load(f)

    latex_wapiti_vulns = []
    for vuln in wapiti_report:
        latex_wapiti_vulns.append(convert_wapiti_vuln_to_latex(vuln))

    with open('wapiti_report.tex', 'w') as f:
        f.write("\n".join(latex_wapiti_vulns))

    # Convert Nikto2 CSV report to LaTeX
    with open('nikto_report.csv', 'r') as f:
        reader = csv.DictReader(f)
        vulns = [row for row in reader]

    latex_nikto_vulns = []
    for vuln in vulns:
        latex_nikto_vulns.append(convert_nikto_vuln_to_latex(vuln))

    with open('nikto_report.tex', 'w') as f:
        f.write("\n".join(latex_nikto_vulns))

    # Convert SQLMap JSON report to LaTeX
    with open('output/output.json', 'r') as f:
        sqlmap_report = json.load(f)

    latex_sqlmap_vulns = []
    for vuln in sqlmap_report:
        latex_sqlmap_vulns.append(convert_sqlmap_vuln_to_latex(vuln))

    with open('sqlmap_report.tex', 'w') as f:
        f.write("\n".join(latex_sqlmap_vulns))

    # Write the main LaTeX document
    main_tex = r"""
\documentclass{article}
\usepackage{hyperref}

\title{Combined Vulnerability Report: Wapiti, Nikto2, and SQLMap}
\author{Your Name}
\date{\today}

\begin{document}

\maketitle

\section{Wapiti Vulnerabilities}
\input{wapiti_report.tex}

\section{Nikto2 Vulnerabilities}
\input{nikto_report.tex}

\section{SQLMap Vulnerabilities}
\input{sqlmap_report.tex}

\end{document}
"""

    with open('combined_report.tex', 'w') as f:
        f.write(main_tex)

    # Compile the LaTeX document to generate the combined PDF report
    subprocess.run(['pdflatex', 'combined_report.tex'])

if __name__ == "__main__":
    main()


