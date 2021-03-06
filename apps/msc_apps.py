#######################################################
#                                                     #
#  Copyright Masterchain Grazcoin Grimentz 2013-2014  #
#  https://github.com/masterchain/masterchain-world   #
#  https://masterchain.info                           #
#  masterchain@@bitmessage.ch                         #
#  https://masterchain.info/LICENSE.txt               #
#                                                     #
#######################################################

import urlparse
import os, sys
from urllib2 import quote
lib_path = os.path.abspath('../../mastercoin-tools')
sys.path.append(lib_path)
from msc_utils_parsing import *

http_status = '200 OK'
error_not_enough_funds = 'Not enough bitcoin funds on address'

def get_response_field(response_dict, field_name):
    return quote(response_dict[field_name][0].strip().encode("utf8"))

def response_with_error(start_response, environ, response_body):
    headers = [('Content-type', 'application/json')]
    start_response(http_status, headers)
    response='{"error":"'+response_body+'"}'
    info(response)
    return response

def general_handler(environ, start_response, response_dict_to_response_func):
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    http_status = 'invalid'
    response_status='OK'
    if method != 'POST':
        return response_with_error(start_response, environ, 'No POST')
    else:
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
        except (TypeError, ValueError):
            return response_with_error(start_response, environ, 'Bad environ in POST')
        try:
            response_dict=urlparse.parse_qs(request_body)
        except (TypeError, ValueError):
            return response_with_error(start_response, environ, 'Bad urlparse')

        (response, error)=response_dict_to_response_func(response_dict)
        if error != None:
            return response_with_error(start_response, environ, error)

        headers = [('Content-type', 'application/json')]
        start_response(http_status, headers)
        return response
