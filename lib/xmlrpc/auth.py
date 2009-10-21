# -*- coding: utf-8 -*-
import gdata.service
import gdata.alt.appengine
import settings

def login_required(pos=1):
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            email = args[pos+0]
            password = args[pos+1]                 
            if is_login(email, password):
                args = args[0:pos]+args[pos+2:]                
                return func(*args, **kwargs)
            else:
                raise ValueError("Authentication Failure")
        return _wrapper
    return _decorate

def author_required(pos=1):
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            email = args[pos+0]
            password = args[pos+1]
            is_author = (settings.AUTHORS.count(email) > 0)
            if is_author and is_login(email, password):
                args = args[0:pos]+args[pos+2:]
                return func(*args, **kwargs)
            else:
                raise ValueError("Authentication Failure")                
        return _wrapper
    return _decorate

def is_login(email, password):
    # Tell the client that we are running in single user mode, and it should not
    # automatically try to associate the token with the current user then store
    # it in the datastore.       
    client = gdata.service.GDataService()
    gdata.alt.appengine.run_on_appengine(client, store_tokens=False, single_user_mode=True)    
    if client.GetClientLoginToken():
        return True
    else:
        client.email = email
        client.password = password
        # To request a ClientLogin token you must specify the desired service using
        # its service name.
        client.service = 'blogger'
        client.source = 'GoogleAPP-niubi-1'
        # Request a ClientLogin token, which will be placed in the client's 
        # current_token member.
        client.ProgrammaticLogin()
        if client.GetClientLoginToken():
            return True
        else:
            return False