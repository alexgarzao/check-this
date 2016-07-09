# -*- encoding: utf-8 -*-
# Check this
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# service_config.py

import logging
from datetime import datetime
import requests


class ServiceConfig:
    '''Class responsible in keep the reminder config.
    '''

    def __init__(self, config, mandrill_service):
        self.logger = logging.getLogger(__name__)

        self.service_name = config.get('service', 'service_name')
        self.template_name = config.get('service', 'template_name')
        self.url = config.get('service', 'url')
        self.expected_result = config.get('service', 'expected_result')
        self.send_resume_to = config.get('service', 'send_resume_to')

        self.mandrill_service = mandrill_service

        return


    def print_config(self):
        self.logger.info('\tService config')
        self.logger.info('\t\tservice_name: %s' % self.service_name)
        self.logger.info('\t\ttemplate_name: %s' % self.template_name)
        self.logger.info('\t\turl: %s' % self.url)
        self.logger.info('\t\texpected_result: %s' % self.expected_result)
        self.logger.info('\t\tsend_resume_to: %s' % self.send_resume_to)

        return


    def check(self):
        self.date_time = datetime.now()
        self.result =  requests.get(self.url).content

        if self.result == self.expected_result:
            self.status = 'OK'
            return True

        self.status = 'ERROR'

        return False


    def summary(self):
        summary = '''
Summary:
    Service name: {}
    Status: {}
    Date/time: {}
    Url: {}
    Expected result: "{}"
    Result: "{}"
'''
        return summary.format(
            self.service_name,
            self.status,
            self.date_time,
            self.url,
            self.expected_result,
            self.result
        )


    def send_notification(self):
        content = [
            {'name': 'service-name', 'content': self.service_name},
            {'name': 'date-time', 'content': self.date_time.strftime("%Y-%m-%d %H:%M:%S")},
            {'name': 'service-url', 'content': self.url},
            {'name': 'expected-result', 'content': self.expected_result},
            {'name': 'result', 'content': self.result},
        ]

        return self.mandrill_service.send(email=self.send_resume_to, name='Service down', template_name=self.template_name, content=content, attachments = None)
