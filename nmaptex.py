import os
import subprocess

def run_nmap(command):
    result = subprocess.run(command.split(), capture_output=True, text=True)
    return result.stdout

def generate_latex(command, output, filename='output.tex'):
    content = r'''\documentclass{article}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{hyperref}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{red},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    numbers=left,
    numbersep=5pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2
}

\lstset{style=mystyle}

\title{Nmap Command for Vulnerability Scanning}
\author{Your Name}
\date{\today}

\begin{document}

\maketitle

\section{Introduction}

This document presents the Nmap command used for scanning a target host for vulnerabilities. Nmap is a powerful and versatile open-source network scanner that can be used to discover hosts and services on a computer network, thus creating a "map" of the network. In this case, we will focus on the command used for vulnerability scanning.

\section{Command}

The following Nmap command is used for vulnerability scanning:

\begin{lstlisting}[language=bash]
%s
\end{lstlisting}

\subsection{Command Explanation}

\begin{itemize}
    \item \texttt{-sV}: This option enables version detection, which helps identify the specific versions of services running on the target host.
    \item \texttt{--script vuln}: This option tells Nmap to run the "vuln" category of scripts from the Nmap Scripting Engine (NSE). These scripts are designed to check for known vulnerabilities in the target host's services.
    \item \texttt{example.org}: This is the target hostname or IP address that you want to scan for vulnerabilities.
\end{itemize}

\section{Example Usage and Result}

Suppose you want to scan "example.org" for vulnerabilities. You would use the following command:

\begin{lstlisting}[language=bash]
%s
\end{lstlisting}

This command will run Nmap with version detection and vulnerability scanning scripts against the target host "example.org". The output will display the discovered services, their versions, and any identified vulnerabilities.

\section{Nmap Output}

Here is the captured Nmap output for the given command:

\begin{lstlisting}
%s
\end{lstlisting}

\end{document}
''' % (command, command, output)

    with open(filename, 'w') as f:
        f.write(content)

def compile_latex(filename):
    basename = os.path.splitext(filename)[0]
        os.system(f'pdflatex {basename}.tex')

if __name__ == '__main__':
    command = 'nmap -sV --script vuln example.org'
    filename = 'output.tex'

    # Run Nmap command and capture the output
    output = run_nmap(command)

    # Generate and compile LaTeX document with Nmap command and its output
    generate_latex(command, output, filename)
    #compile_latex(filename)

