import nmap

def scan_vulnerabilities(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments='-sV --script vuln')
    return scanner

def create_latex_report(scanner, filename):
    with open(filename, "w") as f:
        f.write(r"\documentclass[12pt]{article}" + "\n")
        f.write(r"\usepackage{geometry}" + "\n")
        f.write(r"\geometry{a4paper, margin=1in}" + "\n")
        f.write(r"\usepackage{graphicx}" + "\n")
        f.write(r"\usepackage{booktabs}" + "\n")
        f.write(r"\usepackage{url}" + "\n")
        f.write(r"\usepackage{hyperref}" + "\n")
        f.write(r"\usepackage{listings}" + "\n")
        f.write(r"\title{Vulnerability Scanning Report}" + "\n")
        f.write(r"\author{Your Name}" + "\n")
        f.write(r"\date{\today}" + "\n")
        f.write(r"\begin{document}" + "\n")
        f.write(r"\maketitle" + "\n")
        f.write(r"\section{Introduction}" + "\n")
        f.write("This report presents the results of a vulnerability scanning performed on the target LAMP website, example.com. The scanning was conducted using a Python script leveraging the Nmap tool." + "\n")
        f.write(r"\section{Methodology}" + "\n")
        f.write("The scanning process involved using a Python script that utilized the Nmap library to scan the target website for potential vulnerabilities. The script employed the following Nmap arguments:" + "\n")
        f.write(r"\begin{lstlisting}" + "\n")
        f.write("-sV --script vuln" + "\n")
        f.write(r"\end{lstlisting}" + "\n")
        f.write("These arguments enabled service version detection and vulnerability scanning using Nmap Scripting Engine (NSE) scripts." + "\n")
        f.write(r"\section{Results}" + "\n")
        f.write("The results of the vulnerability scan are presented in the table below:" + "\n")
        f.write(r"\begin{table}[h!]" + "\n")
        f.write(r"\centering" + "\n")
        f.write(r"\begin{tabular}{@{}llll@{}}" + "\n")
        f.write(r"\toprule" + "\n")
        f.write("Host & Protocol & Port & Vulnerabilities \\" + "\\" + "\n")
        f.write(r"\midrule" + "\n")

        for host in scanner.all_hosts():
            for protocol in scanner[host].all_protocols():
                ports = scanner[host][protocol].keys()
                for port in ports:
                    f.write(f"{host} & {protocol} & {port} & \\" + "\\" + "\n")

        f.write(r"\bottomrule" + "\n")
        f.write(r"\end{tabular}" + "\n")
        f.write(r"\caption{Vulnerability scanning results}" + "\n")
        f.write(r"\label{tab:results}" + "\n")
        f.write(r"\end{table}" + "\n")
        f.write(r"\end{document}" + "\n")

if __name__ == "__
