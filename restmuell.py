# coding=utf-8
#Copyright © 2017 razorheadfx <razorhead.effect@gmail.com>
#This work is free. You can redistribute it and/or modify it under the
#terms of the Do What The Fuck You Want To Public License, Version 2,
#as published by Sam Hocevar.
#See http://www.wtfpl.net/ or LICENSE for more details.

from restpusher import RestPusher
import json
from cmd import Cmd
import logging
import sys

log = logging.getLogger(__name__)
frm = '[%(levelname)s] %(module)s.%(funcName)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level = logging.INFO, format = frm)

class RESTMuell(Cmd):
    """ a trashy commandline wrapper for foaas.com's REST API... as a (dis-)service """
    def __init__(self):
        Cmd.__init__(self)
        self.rp = RestPusher("www.foaas.com")
        
        "pull in FOaaS' self description"
        ret = self.rp.get("/operations")
        operation_def = ret["body"]
        
        """
        example from the API self description
        {"name":"Who the fuck are you anyway","url":"/anyway/:company/:from","fields":[{"name":"Company","field":"company"},{"name":"From","fie ld":"from"}]}
        """
        
        "generate do_<operation> functions like Cmd expects them and glue them to this class"
        for jsonNode in operation_def:
            url = jsonNode["url"]
            
            if "-" in url:
                continue
            
            url = url.replace("/", "").split(":")[0]
            
            fields = self.extract_fields(jsonNode)
            name = jsonNode["name"]
            self.make_method(url, name, fields)
            
    def extract_fields(self, json):
        fields = []
        for fieldset in json["fields"]:
            fields.append(fieldset["field"])
        
        return fields
    
    def make_method(self, operation, name, fields = ["none"]):
        """ add a method to the FOaaS class and name do_<operation> """
        """TODO: add argcount checking"""
        methodtemplate = "def do_%s(self, args):\n    '''%s args: %s\n    prints: %s'''\n    self._get('%s',args)\nRESTMuell.do_%s=do_%s"
        
        exec(methodtemplate %(operation,len(fields),fields,name,operation,operation,operation))

           
    def _get(self, operation, args = ""):
        """
        get request
        """
        url = "/"+operation
        if args != "":
            url = url+"/"+args.replace(' ', '/')
            
        ret = self.rp.get(url = url)
        
        print "%s" %ret["body"]["message"]
        print "      -%s" %ret["body"]["subtitle"]
        return 
    
    def do_exit(self, args):
        """exit the shell"""
        print "---- disposing of this trash and exiting."
        sys.exit(0)

if __name__ == "__main__":
    
    muell = RESTMuell()
    muell.prompt = "fuck off as a service>"
    log.debug("%s" %dir(muell)) #log the class signature so we can see which methods have been added
    print "Welcome to RESTMuell the Fuck off-as-a-Service (foaas.com) shell"
    print "---- enter 'help [COMMAND]' to bring up the command reference"
    muell.cmdloop()
    
    
