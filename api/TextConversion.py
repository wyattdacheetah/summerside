from http.server import BaseHTTPRequestHandler
import json
import base64
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

def HandleEmbed( Out, Text, From, To ):
    Out = Out.replace( '<', '' ).replace( '"', '\\"' )
    return f'''<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta name="charset" content="utf-8" />
    <title>Conversion Output From {From} to {To}</title>
    <meta name="title" content="Conversion Output From {From} to {To}">
    <meta name="viewport" content="width=device-width" />

    <meta name="description" content="{Out}" />
    <meta name="author" content="Summer (Wyatt) Da Cheetah" />

    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://summerside.vercel.app/" />
    <meta property="og:title" content="Conversion Output From {From} to {To}" />
    <meta property="og:description" content="{Out}" />
    
    <meta property="twitter:card" content="summary_large_image" />
    <meta property="twitter:url" content="https://summerside.vercel.app/api/TextConversion.py?text={Text}&from={From}&to={To}" />
    <meta property="twitter:title" content="Conversion Output From {From} to {To}" />
    <meta property="twitter:description" content="{Out}" />
  </head>
  <body>{Out}</body>
</html>
'''


def HandleConversion( self, Thing ):
    SupportedTools = [ 'BinaryCode', 'MorseCode', 'Case', 'ASCIICode', 'HexCode', 'Base64', 'text' ]

    From = 'text'
    To = 'text'

    if 'text' not in Thing:
        return EndResponse( self, b'Missing \'text\' parameter', 500 )
    else:
        ToConvert = Thing[ 'text' ]
    
    if 'from' in Thing:
        if not any( a for a in SupportedTools if a == Thing[ 'from' ] ):
          return EndResponse( self, f'From "{Thing[ "from" ]}" tool not found'.encode(), 404 )
        else:
            From = Thing[ 'from' ]

    if 'to' in Thing:
        if not any( a for a in SupportedTools if a == Thing[ 'to' ] ):
            return EndResponse( self, f'Tool "{Thing[ "to" ]}" not found'.encode(), 404 )
        else:
            To = Thing[ 'to' ]

    Output = None

    if From == To:
       Output = ToConvert
    elif From != 'text' and To != 'text':
        Output = ConvertTo( ConvertFrom( ToConvert, From ), To )
    elif From != 'text':
        Output = ConvertFrom( ToConvert, From )
    else:
        Output = ConvertTo( ToConvert, To )
    
    if 'embed' in Thing:
        if Thing[ 'embed' ]:
            Output = HandleEmbed( Output, ToConvert, From, To )
    
    EndResponse( self, Output, MimeType='text/html' if 'embed' in Thing else 'text/plain' )
    
def ConvertTo( What, Method, extras = '' ):
    def ToBinary( ToConvert, extras = extras ):
        BinaryText = [ format( ord( c ), '08b' ) for c in ToConvert ]
        return ''.join( BinaryText ) if extras else ''.join( BinaryText )
    
    def ToHexCode( ToConvert ):
        HexText = [ format( ord( c ), '02x' ) for c in ToConvert ]
        return ' '.join( HexText )
    
    def ToASCIICode( ToConvert ):
        ASCIIText = [ str( ord( c ) ) for c in ToConvert ]
        return ' '.join( ASCIIText )
    
    def ToMorseCode( ToConvert ):
        MorseCodeDict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..'
        }
        MorseText = [ MorseCodeDict.get( c.upper(), '' ) for c in ToConvert ]
        return ' '.join( MorseText )
    
    def ToBase64( ToConvert ):
        return base64.b64encode( ToConvert.encode( 'ascii' ) ).decode( 'ascii' )

    return {
        'BinaryCode': ToBinary,
        'HexCode': ToHexCode,
        'ASCIICode': ToASCIICode,
        'MorseCode': ToMorseCode,
        'Base64': ToBase64
        # TODO: Implement CaseConvert
    }[ Method ]( What )

def ConvertFrom( What, Method ):
    def FromBinary( ToConvert ):
        BinaryText = ToConvert.replace( " ", "" )
        Text = "".join( chr( int( BinaryText[ i : i + 8 ], 2 ) ) for i in range( 0, len( BinaryText ), 8 ) )
        return Text
    
    def FromHexCode( ToConvert ):
        HexText = ToConvert.replace( " ", "" )
        Text = " ".join( chr( int(HexText[ i : i + 2 ], 16 ) ) for i in range( 0, len( HexText ), 2 ) )
        return Text
    
    def FromASCIICode( ToConvert ):
        ASCIIText = ToConvert.split( " " )
        Text = " ".join( chr( int( c ) ) for c in ASCIIText )
        return Text
    
    def FromMorseCode( ToConvert ):
        MorseCodeDict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
            '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
            '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
            '-.--': 'Y', '--..': 'Z'
        }
        MorseText = ToConvert.split(" ")
        Text = " ".join( MorseCodeDict.get( morse, "" ) for morse in MorseText )
        return Text

    def FromBase64( ToConvert ):
        return base64.b64decode( ToConvert.encode( 'ascii' ) ).decode( 'ascii' )
    
    return {
        'BinaryCode': FromBinary,
        'HexCode': FromHexCode,
        'ASCIICode': FromASCIICode,
        'MorseCode': FromMorseCode,
        'Base64': FromBase64
        # TODO: Implement CaseConvert
    }[ Method ]( What )


class handler( BaseHTTPRequestHandler ):
    def do_GET( self ):
        Params = ParseUrl( self.path )
        HandleConversion( self, Params )

    def do_POST( self ):
        ContentLength = int( self.headers[ 'Content-Length' ] )
        JSONBody = json.loads( self.rfile.read( ContentLength ) )
        HandleConversion( self, JSONBody )
