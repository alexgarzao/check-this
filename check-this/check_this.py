# -*- encoding: utf-8 -*-
# Check this
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# check_this.py

import argparse
import ConfigParser
import logging

from service_config import ServiceConfig
from mandrill_service import MandrillService


class Main:
    '''Main class.
    '''

    def __init__(self):
        pass


    def run(self):
        '''Execute the program.
        '''

        self.__log_config()

        self.logger.info('Starting check this...')

        self.__parser_args()
        self.__load_config_file()
        self.__print_config()
        self.__check_service()

        self.logger.info('Check this finishing...')


    def __log_config(self):
        logging.basicConfig(level=logging.INFO)

        self.logger = logging.getLogger(__name__)


    def __parser_args(self):
        '''Define the configuration list.
        '''
        parser = argparse.ArgumentParser(description='Check if a service is ok.')

        parser.add_argument(
                    '--config-file',
                    dest='config_filename',
                    action='store',
                    type=str,
                    help='Config file with the test options',
                    required=True
        )

        self.args = parser.parse_args()

        self.logger.info('Command line configuration')
        self.logger.info('\tConfig file: %s' % self.args.config_filename)


    def __load_config_file(self):
        '''Load the config file specified in --config-file parameter.
        '''
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.args.config_filename)

        self.mandrill_service = MandrillService(self.config)
        self.service_config = ServiceConfig(self.config, self.mandrill_service)


    def __print_config(self):
        '''Print configuration.
        '''
        self.mandrill_service.print_config()
        self.service_config.print_config()

        self.logger.info('\n')


    def __check_service(self):
        '''Check if the service is ok.
        '''

        if self.service_config.check() == True:
            self.logger.info('Service OK:\n%s\n' % self.service_config.summary())
            return

        self.logger.info('Service FAIL::\n%s\n' % self.service_config.summary())

        sent, reject_reason = self.service_config.send_notification()

        if sent == True:
            self.logger.info('Notification sent with success')
        else:
            self.logger.error('Notification rejected: reason=%s' % reject_reason)

        return


if __name__ == "__main__":
    main = Main()
    main.run()
