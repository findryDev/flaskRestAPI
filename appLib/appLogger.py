import logging
from appLib.requestFromApp import getInfo


class appLogger:
    def __init__(self):
        self.loggerRequests = logging.getLogger('flaskRequests')
        self.loggerRequests.setLevel(logging.DEBUG)
        self.file_handler_deb = logging.FileHandler('flaskDeb.log')
        self.deb_format = logging.Formatter(' - %(asctime)s'
                                            ' - %(message)s'
                                            ' - IP:%(ip)s'
                                            ' - method: %(met)s'
                                            ' - endPoint: %(end)s'
                                            ' - %(name)s')
        self.file_handler_deb.setFormatter(self.deb_format)
        self.loggerRequests.addHandler(self.file_handler_deb)
        # loggerErr
        self.loggerError = logging.getLogger('flaskErr')
        self.loggerError.setLevel(logging.ERROR)

        self.file_handler_err = logging.FileHandler('flaskErr.log')

        self.error_format = logging.Formatter('%(levelname)s'
                                              ' - %(asctime)s'
                                              ' - %(message)s'
                                              ' - %(name)s'
                                              ' - IP:%(ip)s'
                                              ' - method: %(met)s'
                                              ' - endPoint: %(end)s')
        self.file_handler_err.setFormatter(self.error_format)
        self.loggerError.addHandler(self.file_handler_err)
        self.loggerDB = logging.getLogger('dbOperation')
        self.loggerDB.setLevel(logging.DEBUG)

        self.file_handler_db = logging.FileHandler('dbLogger.log')

        self.db_format = logging.Formatter(' - %(asctime)s'
                                           ' - %(message)s'
                                           ' - %(name)s'
                                           ' - %(funcName)s')
        self.file_handler_db.setFormatter(self.db_format)
        self.loggerDB.addHandler(self.file_handler_db)

    def createDebLog(self, mess=''):
        extra = getInfo()
        if extra['ip'] != "192.168.0.6":
            self.loggerRequests.debug('flaskApp request ' + mess,
                                      extra=extra)

    def createErrLog(self, err='---'):
        self.loggerError.error(f'flaskApp error: {err}',
                               extra=getInfo())

    def createDBLog(self, dbOperation, value):
        self.loggerDB.debug(f'DB operation {dbOperation} {value}')
