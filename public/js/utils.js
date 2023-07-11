const id = ( a ) => document.getElementById( a );
const WaitFor = ( millis ) => new Promise( (a,_) => setTimeout( a, millis ) );
const locS = ( name, valodflt = "", stt = false ) => {
  if ( stt )
    return localStorage.setItem( document.title + "-" + name, valodflt );
  let a = localStorage.getItem( document.title + "-" + name );
  return a !== undefined ? a : valodflt;
};
const ToChunks = ( a, b ) => {
  let c = [];
  for( let d = 0; d < a.length; d += b )
    c.push( a.slice( d, d + b ) );
  return c;
};