from urllib.parse import urlparse, parse_qs

def ParseUrl( url ):
    parsed_url = urlparse( url )
    query_params = parse_qs( parsed_url.query )

    parameters = {}
    for key, value in query_params.items():
        if len(value) == 1:
            parameters[ key ] = value[0]
        else:
            parameters[ key ] = value

    return parameters

def EndResponse( thingy, Response, ResponseCode: int = 200, MimeType: str = 'text/plain' ):
    if isinstance( Response, str ):
        Response = Response.encode()
        
    thingy.send_response( ResponseCode )
    thingy.send_header( 'Content-Type',  MimeType )
    thingy.end_headers()
    thingy.wfile.write( Response )

def GetContentType( ext ):
    return {
        ".html": "text/html",
        ".htm": "text/html",
        ".md": "text/html",
        ".txt": "text/plain",
        ".css": "text/css",
        ".scss": "text/x-scss",
        ".yml": "text/yaml",
        ".less": "text/less",
        ".js": "text/javascript",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".svg": "image/svg+xml",
        ".xml": "application/xml",
        ".json": "application/json",
        ".map": "application/json",
        ".ttf": "font/ttf",
        ".woff2": "font/woff2"
    }[ ext ]