window.onload = async () => {
  var ToWrite1 = [
    'Hi! Welcome to the Kewl Website I made!',
    'What are the odds of you visiting this site??',
    'Thanks for visiting this website!',
    'Go ahead, choose a tool and use it right away!',
    'Did you know that this changes?? I think so.'
  ];
  num = 0;

  while( true ) {
    ToWrite = ToWrite1[ num ];
    
    while( id( 'WelcomeText' ).innerHTML != '' ) {
      id( 'WelcomeText' ).innerHTML = id( 'WelcomeText' ).innerHTML.slice( 0, id( 'WelcomeText' ).innerHTML.length - 2 );
      await WaitFor( 10 );
    }

    for( let CurrentLetter = 0; CurrentLetter < ToWrite.length; CurrentLetter++ ) {
      let CLetter = ToWrite[ CurrentLetter ];
      id( 'WelcomeText' ).innerHTML += CLetter;
      await WaitFor( [ '?', '.', '!', ',' ].indexOf( CLetter ) > -1 && ToWrite[ CurrentLetter + 1 ] != CLetter ? 800 : 50 );
    }
    num++;
    if ( num == ToWrite1.length )
      num = 0;

    await WaitFor( 3000 );
  }
};