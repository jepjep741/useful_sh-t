import sys
import time
from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print

def main():
    connection = TLSConnection(
        hostname='<your-server-ip>',
        port=9390,
        certfile='/path/to/your/client_cert.pem',
        keyfile='/path/to/your/client_key.pem',
        cafile='/path/to/your/server_ca.pem'
    )

    transform = EtreeTransform()

    gmp = Gmp(connection, transform=transform)

    gmp.authenticate('<openvas-username>', '<openvas-password>')

    target_id = gmp.create_target(
        name='LAMP System',
        hosts=['<lamp-server-ip>'],
        comment='Automated scan of LAMP system'
    )

    config_id = '<full-and-fast-scan-config-id>'
    task_id = gmp.create_task(
        name='LAMP System Scan',
        config_id=config_id,
        target_id=target_id,
        scanner_id='<openvas-scanner-id>'
    )

    gmp.start_task(task_id)

    print(f'Started task with ID: {task_id}')

    while True:
        time.sleep(60)
        task_status = gmp.get_task(task_id)
        status = task_status.xpath('task/status/text()')[0]
        if status == 'Done':
            break

    report_id = task_status.xpath('task/last_report/report/@id')[0]

    report_format_id = '<pdf-report-format-id>'
    export_report = gmp.get_report(
        report_id,
        report_format_id=report_format_id,
        details=True
    )
    report_content = export_report.xpath('report/text()')[0]

    with open('openvas_scan_report.pdf', 'wb') as f:
        f.write(report_content.encode('utf-8'))

    print('Report saved as openvas_scan_report.pdf')

if __name__ == '__main__':
    main()
