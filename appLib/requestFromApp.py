from flask import Flask, request

def getIp():
    return request.remote_addr