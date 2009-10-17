# -*- coding: utf-8 -*-
import gdata.service
import gdata.alt.appengine

def login_required(pos=1):
    def _decorate(method):
        def _wrapper(*args, **kwargs):
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
            client.source = 'GoogleAPP-niubi-1'
            # Request a ClientLogin token, which will be placed in the client's 
            # current_token member.
            client.ProgrammaticLogin()  
            args = args[0:pos]+args[pos+2:]
            if client.GetClientLoginToken():
                raise ValueError("Authentication Failure")
            return method(*args, **kwargs)
        return _wrapper
    return _decorate