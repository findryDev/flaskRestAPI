from flask import request


def getInfo():
    return {'ip': request.remote_addr,
            'met': request.method,
            'end': request.endpoint}
