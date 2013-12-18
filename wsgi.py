import wsgiref.simple_server as simple_server
import cgi
import sys
from weberror import evalexception

port = int(sys.argv[1])
### part1
def hello(environ, start_response):
    u'''
    return Hello world
    '''

    start_response('200 OK', [('Content-Type', 'text/plain')])

    return ['Hello, World']

def run(app):
    server = simple_server.make_server('', port, app)
    server.serve_forever()

### part2
def calc_fib(value):
    x,y = 0,1
    
    for x in range(value):
        x,y =y, x+y
    
    return x

def fib(environ, start_response):
    '''
    calculate fibonach and return
    '''
    fs = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
    
    #take parameter "value"
    value = fs.getfirst('value', '0')
    
    val = int(value)
    result = calc_fib(val)
    start_response('200 OK', [('Content-Type', 'text/plain')])

    return [str(result)]

def url_mapping(environ, start_response):
    u'''
    try url mapping
    '''
    # path when it is called
    script_path = environ['SCRIPT_NAME']

    # information of path
    path = environ['PATH_INFO']

    if path == '/fib':
        # calc fib
        return fib(environ, start_response)
    else:
        # hello, world
        return hello(environ, start_response)
    
def mapping(patterns, default = None):
    '''
    
    '''
    def internal(environ, start_response):
        path = environ['PATH_INFO']
        
        if path in patterns:
            return patterns[path](environ, start_response)
        elif default is not None:
            return default(environ, start_response)
        start_response('404 NotFound', [('Content-Type', 'text/plain')])

    return internal



    
if __name__ == '__main__':
#    run(hello)
#    run(fib)
#    run(url_mapping)
    app = mapping({'/fib':fib}, hello)
    run(evalexception.EvalException(app))
