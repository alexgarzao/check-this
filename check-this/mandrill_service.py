# -*- encoding: utf-8 -*-
# Check this
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# mandrill_service.py

import logging
import mandrill


class MandrillService:
    '''Class responsible in send emails using the mandrill service.
    '''

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        self.api_key = config.get('mandrill', 'api_key')

        try:
            self.mandrill_client = mandrill.Mandrill(self.api_key)
        except mandrill.Error, e:
            self.logger.error('A mandrill error occurred: %s - %s' % (e.__class__, e))
            raise

        return


    def print_config(self):
        self.logger.info('\tMandrill service config')
        self.logger.info('\t\tapi_key: %s' % self.api_key)

        return


    def send(self, email, name, template_name, content, subject = None, attachments = None):
        '''Send the email using the defined template.
        '''

        message = {
            'attachments': attachments,
            'global_merge_vars': content,
            'important': False,
            'merge': True,
            'merge_language': 'handlebars',
            'to': [{'email': email, 'name': name, 'type': 'to'}],
            'subject': subject,
        }

        try:
            result = self.mandrill_client.messages.send_template(
                template_name=template_name,
                template_content=None,
                message=message,
                async=False,
                ip_pool='Main Pool')

            sent_status = result[0]['status']
            sent_reject_reason = ''

            if 'reject_reason' in result[0]:
                sent_reject_reason = result[0]['reject_reason']

            return (sent_status == 'sent' or sent_status == 'queued'), sent_reject_reason

        except mandrill.Error, e:
            self.logger.info('A mandrill error occurred: %s - %s' % (e.__class__, e))
            return False
