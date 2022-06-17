function generateTransitionArray(nSwitches) {
  // Takes as input the number of switches that should occur out of 16 total transitions
  // Returns an array of length 17 where each element is string containing a color: 'red' or 'blue'
    // Where the number of switches between colors equals nSwitches

  // Initialize array with values 1:16 to use as indices
  var indicesContainer = []
  for (i = 1; i < 17; i++) {
    indicesContainer[i-1] = i; 
  }

  // Initialize out vector with random starting color
  var out = [];
  out[0] = Math.random(1) > .5 ? 'blue' : 'red';

  // Start everything at repeat
  for (i = 0; i < 17; i++) {
    if (i) {
      out[i] = 'repeat';
    }
  }

  // Randomly set nSwitch number of elements in out to switch
  for (i = 0; i < nSwitches; i++) {
    out[getRandomFromBucket(indicesContainer)] = 'switch';
  }

  // Convert 'switch' and 'repeat' to their color values based on the starting color
  for (i = 1; i < out.length; i++) {
    if (out[i] == 'repeat') {
      out[i] = out[i-1];
    } else {
      out[i] = out[i-1] == 'red' ? 'blue' : 'red';
    }
  }

  return out;

} // end generateTransitionArray()

function getRandomFromBucket(bucket) {
  var randomIndex = Math.floor(Math.random()*bucket.length);
  return bucket.splice(randomIndex, 1)[0];
}


function createConditionOrder() {
  // Returns an array of dicts
  // Where each dict:
    // {'id': 'HE', 'pSwitch': {'safe': 11, 'risky': 14}}

  var conditionHolder = [
    {
      'name': 'HE',
      'pSwitch': {'safe': 11, 'risky': 14}
    },

    {
      'name': 'HM',
      'pSwitch': {'safe': 10, 'risky': 12}
    },

    {
      'name': 'EE',
      'pSwitch': {'safe': 5, 'risky': 2}
    },

    {
      'name': 'EM',
      'pSwitch': {'safe': 6, 'risky': 4}
    }
  ]

  var conditionOrder = []

  for (i = 0; i < 4; i++) {
    conditionOrder.push(getRandomFromBucket(conditionHolder));
  }

  return conditionOrder;

}

function getDeckCode(currentCondition) {
  // Takes in current condition (see above)
  // Returns an object sorting the current condition by deck parameters
    // {'left': {'name:' 'risky', 'pSwitch': {'top': 8, 'bottom': 14}}}

  // Initialize the two decks
  var riskyDeck = {'name': 'riskyDeck'};
  var safeDeck = {'name': 'safeDeck', 'pSwitch': {'top': currentCondition['pSwitch']['safe']}};

  // Determine the location (top / bottom) for the two outcomes of the risky deck randomly
  var top = Math.random() > .5 ? 8 : currentCondition['pSwitch']['risky'];
  var bottom = top == 8 ? currentCondition['pSwitch']['risky'] : 8;

  // Assign them to riskyDeck
  riskyDeck['pSwitch'] = {'top': top, 'bottom': bottom};

  // Shuffle left/right and return
  return getDeckLocation(riskyDeck, safeDeck, '', 2);

}


function determineOutcomePswitch(chosenDeckLocation, deckCode) {
  // Takes in the chosen deck location and deckCode (obv)
  // Returns dict containing selected pSwitch and the spatial position of the selected outcome:
    // {'pSwitch': 8, 'horizontal': 'left', 'vertical': 'top'}

  var out = {'horizontal': chosenDeckLocation};

  if (deckCode[chosenDeckLocation]['name'] == 'safeDeck') {
    out['vertical'] = 'Top';
    out['pSwitch'] = deckCode[chosenDeckLocation]['pSwitch']['top'];
  } else {
    if (Math.random() > .5) {
      out['pSwitch'] = deckCode[chosenDeckLocation]['pSwitch']['top']
      out['vertical'] = 'Top';
    } else {
      out['pSwitch'] = deckCode[chosenDeckLocation]['pSwitch']['bottom']
      out['vertical'] = 'Bottom';
    }
  }

  return out;

}

function updateDeckAttributes(deckCode, corrected) {
  // Fill deck attributes
  $('#leftDeckTop').html('<p>' + translateSwitchForDisplay(deckCode['left']['pSwitch']['top'], corrected) + '</p>');
  $('#rightDeckTop').html('<p>' + translateSwitchForDisplay(deckCode['right']['pSwitch']['top'], corrected) + '</p>');

  if (deckCode['left']['name'] == 'riskyDeck') {
    $('#leftDeckBottom').html('<p>' + translateSwitchForDisplay(deckCode['left']['pSwitch']['bottom'], corrected) + '</p>');
    activeSeparator = 'left';
  } else {
    $('#rightDeckBottom').html('<p>' + translateSwitchForDisplay(deckCode['right']['pSwitch']['bottom'], corrected) + '</p>');
    activeSeparator = 'right';
  }

  return activeSeparator;

}

function translateSwitchForDisplay(pSwitch, corrected) {
  if (corrected == 'true') {
    translation_dict = {8: '0',
                    4: '-24',
                    6: '-12',
                    10: '+12',
                    12: '+24',
                    5: '-18',
                    2: '-36',
                    11: '+18',
                    14: '+36'};

    return translation_dict[pSwitch]
  }

  var out = '';

  // if it's reference, keep label at 50
  if (pSwitch == 8) {
    out += '0';

  } else {
    // else, add the absolute units on to out first
    absUnits = Math.floor(pSwitch * 6.25);
    absUnits = pSwitch < 8 ? absUnits + 1 : absUnits;
    
    // omitting this information
    //out += absUnits;

    // then code the direction of shift from reference
    if (pSwitch > 8) {
      out += '+';
    } else {
      out += '-';
    }

    // then add the difference
    subUnits = Math.abs(absUnits - 50);
    out = out + String(subUnits);

  }
  return out;
}



function updateAttributeColors(deckCode){
  // clumsy approach, but it should work

  // if left deck is safe deck
  if (deckCode['left']['name'] == 'safeDeck') {

    updateParam = deckCode['right']['pSwitch']['top'] == 8 ? 'bottom' : 'top';
    blackParam = updateParam == 'bottom' ? 'top' : 'bottom';

    // if all losses, make font red
    if (deckCode['left']['pSwitch']['top'] > 8) {
      $('#leftDeckTop').css({'color': 'rgb(' + String(translateSwitchToColor(deckCode['left']['pSwitch']['top'])) + ', 0, 0)'});
      $('#rightDeck' + jsUcfirst(updateParam)).css({'color': 'rgb(' + String(translateSwitchToColor(deckCode['right']['pSwitch'][updateParam])) + ', 0, 0)'});

    // if all gains, make font green
    } else {
      $('#leftDeckTop').css({'color': 'rgb(0, ' + String(translateSwitchToColor(deckCode['left']['pSwitch']['top'])) + ', 0)'});
      $('#rightDeck' + jsUcfirst(updateParam)).css({'color': 'rgb(0, ' + String(translateSwitchToColor(deckCode['right']['pSwitch'][updateParam])) + ', 0)'});
    }

    $('#rightDeck' + jsUcfirst(blackParam)).css({'color': 'black'});

  
  // if right deck is safe deck
  } else {

    updateParam = deckCode['left']['pSwitch']['top'] == 8 ? 'bottom' : 'top';
    blackParam = updateParam == 'bottom' ? 'top' : 'bottom';

    // if all losses, make font red
    if (deckCode['right']['pSwitch']['top'] > 8) {
      $('#rightDeckTop').css({'color': 'rgb(' + String(translateSwitchToColor(deckCode['right']['pSwitch']['top'])) + ', 0, 0)'});
      $('#leftDeck' + jsUcfirst(updateParam)).css({'color': 'rgb(' + String(translateSwitchToColor(deckCode['left']['pSwitch'][updateParam])) + ', 0, 0)'});

    // if all gains, make font green
    } else {
      $('#rightDeckTop').css({'color': 'rgb(0, ' + String(translateSwitchToColor(deckCode['right']['pSwitch']['top'])) + ', 0)'});
      $('#leftDeck' + jsUcfirst(updateParam)).css({'color': 'rgb(0, ' + String(translateSwitchToColor(deckCode['left']['pSwitch'][updateParam])) + ', 0)'});
    }

    $('#leftDeck' + jsUcfirst(blackParam)).css({'color': 'black'});

  }

}

function translateSwitchToColor(pSwitch) {
  // making it so that the ends of the switching limits that subjects will see in the exp (i.e., 2 and 14) correspond to the ends of the color spectrum
  // thus, need to chop the spectrum in any one direction (255) into the number of segments equal to the 
  // absolute value of the difference between the end of switching and reference (eg, 14-8 = 6)
  // function behaves incorrectly for input 8, but that's okay

  colorMin = 100;
  colorMax = 200;

  return (((colorMax - colorMin) / 6) * Math.abs(pSwitch - 8)) + colorMin;
}

function jsUcfirst(string) {
  // capitalize first letter of string
  return string.charAt(0).toUpperCase() + string.slice(1);
}


// OCT 25, 2021 ADDITIONS FOR PY POOL
function getParam( name, defaultValue ) { 
   var regexS = "[\?&]"+name+"=([^&#]*)"; 
   var regex = new RegExp( regexS ); 
   var tmpURL = window.location.href; 
   var results = regex.exec( tmpURL ); 
   if( results == null ) { 
     return defaultValue; 
   } else { 
     return results[1];    
   } 
}