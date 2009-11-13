from gdataRequest import Client

def login_required(pos=1):
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            client = Client(email=args[pos+0], password=args[pos+1])
            if client.is_authenticated():
                args = args[0:pos]+args[pos+2:]                
                return func(*args, **kwargs)
            else:
                raise ValueError("Authentication Failure")
        return _wrapper
    return _decorate

def author_required(pos=1):
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            client = Client(email=args[pos+0], password=args[pos+1])
            if client.is_author() and client.is_authenticated():
                args = args[0:pos]+args[pos+2:]
                return func(*args, **kwargs)
            else:
                raise ValueError("Authentication Failure")                
        return _wrapper
    return _decorate