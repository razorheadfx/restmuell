#Copyright © 2017 razorheadfx <razorhead.effect@gmail.com>
#This work is free. You can redistribute it and/or modify it under the
#terms of the Do What The Fuck You Want To Public License, Version 2,
#as published by Sam Hocevar.
#See http://www.wtfpl.net/ or LICENSE for more details.

import httplib
import json
import logging
import sys

log = logging.getLogger(__name__)
frm = '[%(levelname)s] %(module)s.%(funcName)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level = logging.WARN, format = frm)

class RestPusher:
    """ a simple wrapper for post/put/get/delete http requests"""
    def __init__(self, server, port = 80):
        self.server = server
        self.port = port
    
    def set_server(self, serveraddress):
        """
        change the target hostname/ip addr to the given one
        :param server, address of the server
        """
        assert(type(serveraddress) == str)
        self.server = serveraddress
    
    def get(self, url, data = None, headers = None):
        """ perform a get request
        :param url
        :param object/dict, which will be dumped using json.dumps
        :param dict of header settigs i.e.  Content-type : application/json
        """
        
        ret = self._rest_call(url, data, 'GET', headers)
        return ret
  
    def post(self, url, data):
        
        ret = self._rest_call(url, data, "POST", headers = None)
        return ret
    
    def put(self, url, data, headers = None):
        """ perform a put request
        :param url
        :param object/dict, which will be dumped using json.dumps
        :param dict of header settigs i.e.  Content-type : application/json
        """
        ret = self._rest_call(url, json, "PUT", headers = None)
        return ret
    
    def delete(self, url, data = None, headers = None):
        ret = self._rest_call(url, data, "DELETE", headers)
        return ret
  
    def _rest_call(self, url, data, action, headers = None):
        assert(action in ["GET","PUT","POST","DELETE"])
        assert(url != None)
        
        """use json by default"""
        if headers == None:
            headers = {"Content-type": "application/json","Accept": "application/json"}
            
        if data != None:
            reqbody = data.dumps(data)
        else:
            reqbody = None
        
        log.debug("Calling to " +self.server+url)
        
        con = httplib.HTTPConnection(self.server, self.port)
        con.request(action, url, body = reqbody, headers =  headers)
        response = con.getresponse()        
        
        if response.status != 200:
            log.error("Non 200 statuscode: %s for request %s:%s/%s\n body:%s headers: %s" %(response.status,action, self.server, url, reqbody, headers))
        
        
        try:
            body = json.loads(response.read())
                    
        except:
            body = None
            log.error("An error occoured while parsing the returned JSON")
        
        resp_data = {"statuscode": response.status, "body" : body, "headers" : response.getheaders()}
        log.debug("%s" %resp_data)

        con.close()
        
        return resp_data