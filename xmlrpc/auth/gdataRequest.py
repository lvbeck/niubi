import lib.vendor.google.gdata.service
import lib.vendor.google.gdata.alt.appengine
import settings

class Client(object):
    
    email = ''
    password = ''
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def is_authenticated(self):
        # Tell the client that we are running in single user mode, and it should not
        # automatically try to associate the token with the current user then store
        # it in the datastore.       
        client = gdata.service.GDataService()
        gdata.alt.appengine.run_on_appengine(client, store_tokens=False, single_user_mode=True)    
        if client.GetClientLoginToken():
            return True
        else:
            client.email = self.email
            client.password = self.password
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
    
    def is_author(self):
        return (settings.AUTHORS.count(self.email) > 0)
        