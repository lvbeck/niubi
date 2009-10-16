# -*- coding: utf-8 -*-
import gdata.service
import gdata.alt.appengine
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

def login_required(func):
    def _wrapper(*args, **kw):
        # Tell the client that we are running in single user mode, and it should not
        # automatically try to associate the token with the current user then store
        # it in the datastore.        
        client = gdata.service.GDataService()
        gdata.alt.appengine.run_on_appengine(client, store_tokens=False, single_user_mode=True)
        client.email = args[pos+0]
        client.password = args[pos+1]
        # To request a ClientLogin token you must specify the desired service using
        # its service name.
        client.service = 'blogger'
        client.source = 'GoogleInc-niubi-1'
        # Request a ClientLogin token, which will be placed in the client's 
        # current_token member.
        client.ProgrammaticLogin()
        if client.GetClientLoginToken():
            return func(*args, **kw)
        else:
            raise ValueError("Authentication Failure")
    return _wrapper