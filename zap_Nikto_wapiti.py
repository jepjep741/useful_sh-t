import subprocess
import time
from zapv2 import ZAPv2
from jinja2 import Environment, FileSystemLoader

# Config
target_url = 'http://example.com'
zap_api_key = 'your_zap_api_key'
zap_host = 'http://127.0.0.1'
zap_port = 8080

# Initialize ZAP
zap = ZAPv2(apikey=zap_api_key, proxies={'http': f'{zap_host}:{zap_port}', 'https': f'{zap_host}:{zap_port}'})

# Run ZAP Spider and Active Scan
print("Starting the ZAP spider...")
spider_scan_id = zap.spider.scan(target_url)
while int(zap.spider.status(spider_scan_id)) < 100:
    time.sleep(10)
print("ZAP spider completed.")

print("Starting the ZAP active scan...")
active_scan_id = zap.ascan.scan(target_url)
while int(zap.ascan.status(active_scan_id)) < 100:
    time.sleep(10)
print("ZAP active scan completed.")

# Run Nikto Scan
print("Starting Nikto scan...")
nikto_command = f"nikto -h {target_url} -o nikto_report.txt"
nikto_result = subprocess.run(nikto_command, shell=True, text=True, capture_output=True)
if nikto_result.returncode != 0:
    print("An error occurred while running the Nikto scan.")
else:
    print("Nikto scan completed.")

# Run Wapiti Scan
print("Starting Wapiti scan...")
output_dir = 'wapiti_output'
wapiti_command = f"wapiti {target_url} -o {output_dir}"
wapiti_result = subprocess.run(wapiti_command, shell=True, text=True, capture_output=True)
if wapiti_result.returncode != 0:
    print("An error occurred while running the Wapiti scan.")
else:
    print("Wapiti scan completed.")

# Generate LaTeX Report
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("report_template.tex")

report_data = {
    "target_url": target_url,
    "zap_spider": zap.spider.results(spider_scan_id),
    "zap_alerts": zap.core.alerts(),
    "nikto_output": nikto_result.stdout,
    "wapiti_output": wapiti_result.stdout,
}

with open("report.tex", "w") as report_file:
    report_file.write(template.render(report_data))

# Compile LaTeX to PDF
print("Generating PDF report...")
latex_command = "pdflatex report.tex"
result = subprocess.run(latex_command, shell=True, text=True)
if result.returncode != 0:
    print("An error occurred while generating the PDF report.")
else:
    print("PDF report generated.")
