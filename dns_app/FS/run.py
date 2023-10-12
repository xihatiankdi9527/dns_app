from flask import Flask
from socket import *
import logging

app = Flask (__name__)
logging.getLogger().setLevel(logging.DEBUG)


def fibnacci_calc(b):
    if b < 0:
        logging.info("Number should be greater than 0")
    elif b == 1:
        return 0
    elif b == 2:
        return 1
    else:
        return fibnacci_calc( b-1 ) + fibnacci_calc( b-2 )
