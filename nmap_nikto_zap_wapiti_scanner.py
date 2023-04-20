import os
import subprocess
import time
from zapv2 import ZAPv2
from urllib.parse import urlparse

target_url = 'http://example.com'
parsed_url = urlparse(target_url)
server_name = parsed_url.hostname
output_folder = 'output'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Nmap Scan
nmap_output = os.path.join(output_folder, 'nmap.txt')
nmap_command = f'nmap -sV {server_name} -oN {nmap_output}'
subprocess.run(nmap_command, shell=True)

# Nikto Scan
nikto_output = os.path.join(output_folder, 'nikto.txt')
nikto_command = f'nikto -h {target_url} -output {nikto_output}'
subprocess.run(nikto_command, shell=True)

# SQLMap Scan
sqlmap_output = os.path.join(output_folder, 'sqlmap.txt')
sqlmap_command = f'sqlmap -u "{target_url}" --batch --dbs --output={sqlmap_output}'
subprocess.run(sqlmap_command, shell=True)

# OWASP ZAP Scan
zap = ZAPv2(proxies={'http': 'http://localhost:8080', 'https': 'http://localhost:8080'})
zap.spider.scan(target_url)
while int(zap.spider.status()) < 100:
    time.sleep(10)
zap.ascan.scan(target_url)
while int(zap.ascan.status()) < 100:
    time.sleep(10)
zap.core.xmlreport(file=os.path.join(output_folder, 'zap.xml'))

# Wapiti Scan
wapiti_output = os.path.join(output_folder, 'wapiti')
wapiti_command = f'wapiti -u {target_url} -o {wapiti_output}'
subprocess.run(wapiti_command, shell=True)

# Generate LaTeX Report
latex_report = os.path.join(output_folder, 'report.tex')

with open(latex_report, 'w') as report:
    report.write('\\documentclass{article}\n')
    report.write('\\usepackage{listings}\n')
    report.write('\\lstset{basicstyle=\\footnotesize\\ttfamily,breaklines=true}\n')
    report.write('\\title{Security Scan Report}\n')
    report.write('\\begin{document}\n')
    report.write('\\maketitle\n')

    def write_section(header, content):
        report.write('\\section*{' + header + '}\n')
        report.write('\\begin{lstlisting}\n')
        report.write(content)
        report.write('\\end{lstlisting}\n')

    with open(nmap_output, 'r') as nmap_results:
        write_section("Nmap Scan", nmap_results.read())

    with open(nikto_output, 'r') as nikto_results:
        write_section("Nikto Scan", nikto_results.read())

    with open(sqlmap_output, 'r') as sqlmap_results:
        write_section("SQLMap Scan", sqlmap_results.read())

    with open(os.path.join(output_folder, 'zap.xml'), 'r') as zap_results:
        write_section("OWASP ZAP Scan", zap_results.read())

    write_section("Wapiti Scan", f"Check the Wapiti output folder for detailed results: {wapiti_output}")

    report.write('\\end{document}\n')

# Compile LaTeX to PDF
pdf_report = os.path.join(output_folder, 'report.pdf')
pdflatex_command = f'pdflatex -output-directory={output_folder} {latex_report}'
subprocess.run(pdflatex_command, shell=True)

# Remove auxiliary files
