from http.server import BaseHTTPRequestHandler
import socketserver
import importlib.util
from utils import GetContentType, EndResponse
from os.path import isdir, exists

PORT = 80

def HandleAPI( self, filename ):
    try:
        spec = importlib.util.spec_from_file_location( 'module', filename )
        module = importlib.util.module_from_spec( spec )
        spec.loader.exec_module( module )

        handler = module.HttpHandler
        handler.do_GET( self )
    except FileNotFoundError:
        self.send_response( 404 )
        self.send_header( 'Content-Type', 'text/plain' )
        self.end_headers()
        self.wfile.write( f'File not found {filename}'.encode() )

class HttpHandler( BaseHTTPRequestHandler ):
    def do_GET( self ):
        url = 'public' + self.path
        if '?' in url:
            url = url[ :url.index( '?' ) ]

        try:
            if url.startswith( 'public/api/' ):
                return HandleAPI( self, url )
            
            if not isdir( url ):
                with open( url, 'rb' ) as file:
                    self.send_response( 200 )
                    self.send_header('Content-type', GetContentType( url[ url.rindex( '.' ): ] ) )
                    self.end_headers()
                    self.wfile.write( file.read() )
            else:
                if not exists( url + 'index.html' ):
                    EndResponse( self, b'no.', 403 )
                else:
                    with open( url + 'index.html', 'rb' ) as file:
                        self.send_response( 200 )
                        self.send_header('Content-type', 'text/html' )
                        self.end_headers()
                        self.wfile.write( file.read() )

        except IOError:
            EndResponse( self, b'Path not found!!', 404 )
    
    def do_POST( self ):
        url = 'public' + self.path
        if '?' in url:
            url = url[ :url.index( '?' ) ]

        if url.startswith( 'public/api/' ):
            return HandleAPI( self, url )
        else:
            EndResponse( self, 'no.', 403 )

with socketserver.TCPServer(("", PORT), HttpHandler) as httpd:
    print("Server running on port", PORT)
    httpd.serve_forever()
