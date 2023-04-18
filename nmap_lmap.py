# nmap --script-updatedb
#pip3 install pylatex python-nmap

import nmap
from pylatex import Document, Section, Subsection, Table, Package
from pylatex.utils import bold

def scan_vulnerabilities(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments='-sV --script vuln')
    return scanner

def create_latex_report(scanner, filename):
    doc = Document()

    # Add packages
    doc.packages.append(Package("geometry", options="a4paper, margin=1in"))
    doc.packages.append(Package("graphicx"))
    doc.packages.append(Package("booktabs"))
    doc.packages.append(Package("url"))
    doc.packages.append(Package("hyperref"))
    doc.packages.append(Package("listings"))

    # Add title
    doc.preamble.append(Command('title', 'Vulnerability Scanning Report'))
    doc.preamble.append(Command('author', 'Your Name'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    # Add content
    with doc.create(Section("Introduction")):
        doc.append("This report presents the results of a vulnerability scanning performed on the target LAMP website, example.com. The scanning was conducted using a Python script leveraging the Nmap tool.")

    with doc.create(Section("Methodology")):
        doc.append("The scanning process involved using a Python script that utilized the Nmap library to scan the target website for potential vulnerabilities. The script employed the following Nmap arguments:")
        doc.append(NoEscape(r'\begin{lstlisting}'))
        doc.append("-sV --script vuln")
        doc.append(NoEscape(r'\end{lstlisting}'))
        doc.append("These arguments enabled service version detection and vulnerability scanning using Nmap Scripting Engine (NSE) scripts.")

    with doc.create(Section("Results")):
        doc.append("The results of the vulnerability scan are presented in the table below:")
        with doc.create(Table(position='h!')) as table:
            table.append(NoEscape(r'\centering'))
            table.append(Command('caption', "Vulnerability scanning results"))
            table.append(NoEscape(r'\label{tab:results}'))
            with doc.create(Tabular('|l|l|l|l|')) as tabular:
                tabular.add_hline()
                tabular.add_row((bold("Host"), bold("Protocol"), bold("Port"), bold("Vulnerabilities")))
                tabular.add_hline()
                for host in scanner.all_hosts():
                    for protocol in scanner[host].all_protocols():
                        ports = scanner[host][protocol].keys()
                        for port in ports:
                            tabular.add_row((host, protocol, port, ""))
                tabular.add_hline()

    # Save the document
    doc.generate_pdf(filename, clean_tex=False)

if __name__ == "__main__":
    target = "example.com"  # Replace with the target LAMP website
    scanner = scan_vulnerabilities(target)
    create_latex_report(scanner, "vulnerability_report")
