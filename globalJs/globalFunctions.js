// FOR DEMO
function parseDemos(x) {
  var race = [];
  var holder = [];

  for (foo = 0; foo < x.length; foo++) {
    // if we're dealing with race
    if (foo == 1) {
      // and race has values
      if (x[foo].length > 0) {
        // be ready to parse out more than one value
        for (bar = 0; bar < x[1].length; bar++) {
        race.push(x[foo][bar]['value']);
        }
        // convert it to a flat string
        race = race.toString();
      } else {race = 'na'}
      holder.push(race);
    } else {
      if (x[foo].length > 0) {
        holder.push(x[foo].val());
      } else {holder.push('na')}
    } 
  } // end global for

  return holder;
}

function generateCuedStim() {
  // takes as input nothing
  // returns a random digit between 1 and 9 (inclusive) excluding 5
  var stim = Math.floor(Math.random() * 8) + 1

  if (stim >= 5) {
    stim += 1;
  }
  return stim;
}

function generateTransition(pSwitch, prevTaskColor) {
  // takes as input probability of switch and the previous task (cue color)
  // returns color for upcoming stimulus

  var out = '';

  // if there is a previous task
  if (prevTaskColor) {
    // a random event greater than pSwitch threshold represents a repeat
    if (Math.random() > pSwitch) {
      out = prevTaskColor;
      // otherwise, it's a switch
    } else {
      out = prevTaskColor == 'blue' ? 'red' : 'blue';
    }
    // otherwise, generate as if a coin flip
  } else {
      out = Math.random() > .5 ? 'red' : 'blue';
  }
  return out;
}

// counterbalance task cue

function createTaskCue() {
  // randomly determines for each subject which color represents which task

  var out = {};

  if (Math.random() > .5) {
    out = {'blue': 'mag', 'red': 'par'};
  } else {
    out = {'blue': 'par', 'red': 'mag'};
  }
  return out;
}


function createClientCueText(taskCueCode) {
  // takes as input {'blue': 'par', etc}
  // returns dict with client facing text

  var out = {};

  if (taskCueCode['blue'] == 'par') {
    out['blue'] = 'Parity';
    out['red'] = 'Magnitude';
  } else {
    out['blue'] = 'Magnitude';
    out['red'] = 'Parity';
  }

  return out;

}



// cued task switching error check

function cuedIsError(key, currentTask, currentStim) {
  // takes as input:
    // key: the number key [74, 75] that was pressed
    // currentTask: 'par' or 'mag'
    // taskCueCode: dict mapping color to task
      // eg: {'blue': 'mag' ... etc}
  // returns: error = [0 | 1] 

  // for now, im assuming that (for par) 74 (j) is odd and 75 (k) is even

  var error = 0;

  // searching for cases where errors are committed
  if (currentTask == 'par') {
    if (currentStim % 2 && key == 75) {
      error = 1;
    } else if (currentStim % 2 == 0 && key == 74) {
      error = 1;
    } 

  } else if (currentTask == 'mag') {
    if (currentStim < 5 && key == 75) {
      error = 1;
    } else if (currentStim > 5 && key == 74) {
      error = 1;
    }

  } else {
    console.log('Something with if/else handling failed in cuedIsError()');
  }

  return error;

}


function codeTransition(prevTaskColor, currentTaskColor) {
  // takes as input previous task and current task
  // returns string indicating whether current task is switch or repeat

  var out = '';

  if (prevTaskColor) {
    out = prevTaskColor == currentTaskColor ? 'repeat' : 'switch';
  } else {
    out = 'startBlock';
  }

  return out;
}

function parseUrl(name) {
  // function takes as input argument name and returns results formatted for urlArgsToDict
  // kinda messy tbh

  // is it a dict?
  var d = 0;
  // if the name corresponds to a dict
  if (name == 'taskCueCode' || name == 'rtPercentiles') {
    d = 1;
    var regexS = '[\?&](' + name + '.*?&' + name + '.*?[^&]*)'
  } else {
    var regexS = "[\?&]"+name+"=([^&#]*)"; 
  }

  // execute regex
  var regex = new RegExp(regexS);
  var tmpUrl = window.location.href;
  var results = regex.exec(tmpUrl);

  if (results == null) {
    return 'NONE';
  } else {
    // if dict, deparam the results
    if (d) {
      return $.deparam(results[1]);
    } else {
      return results[1];
    }
  }
}

function urlArgsToVar(name) {
  // takes as input 
  var results = parseUrl(name);

  // if it's a dict, index it
  if (typeof(results) == 'object') {
    return results[name];
  } else {
    // if it's the time, convert to int
    if (name == 'experimentStartTime') {
      return parseInt(results);
    } else {
      return results;
    }
  }
}

// specific to DECKS

function rnorm() {
  // draw from normal distribution with mean 0 and var 1
  var u = 0, v = 0;
  while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
  while(v === 0) v = Math.random();
  return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
}


function getDeckLocation(deckOne, deckTwo, deckThree, nDecks) {
  // takes as input deckCode and number of decks
  // returns deckCode updated with location

  var deckCode = {};

  if (nDecks == 2) {
    // if it's practice, just randomly generate location
    if (Math.random() < .5) {
      deckCode['left'] = deckOne;
      deckCode['right'] = deckTwo;
    } else {
      deckCode['left'] = deckTwo;
      deckCode['right'] = deckOne;
    }
  
  } else if (nDecks == 3) {
    var container = [deckOne, deckTwo, deckThree];
    deckCode['left'] = getRandomFromBucket(container);
    deckCode['right'] = getRandomFromBucket(container);
    deckCode['middle'] = getRandomFromBucket(container);
  }

  return deckCode;

}

function getRandomFromBucket(bucket) {
  // from: https://stackoverflow.com/questions/12987719/javascript-how-to-randomly-sample-items-without-replacement
  // don't run more times than length of the bucket being indexed
  var randomIndex = Math.floor(Math.random()*bucket.length);
  return bucket.splice(randomIndex, 1)[0];
}


function getChosenDeckLocation(key, phase){
  // determine chosen deck location
  var chosenDeckLocation = '';

  if (phase == 'twoChoice') {
    if (key == 68){
      chosenDeckLocation = 'left';
    } else if (key == 70) {
      chosenDeckLocation = 'right';
    } else {
      console.log('something went wrong determining the location of the chosen deck');
      chosenDeckLocation = Math.random() > .5? 'left' : 'right';
    }
  // if it's three choice, we need to handle three locations
  } else if (phase == 'threeChoice') {
    if (key == 83) {
      chosenDeckLocation = 'left';
    } else if (key == 68) {
      chosenDeckLocation = 'middle';
    } else if (key == 70) {
      chosenDeckLocation = 'right';
    }
  }

  return chosenDeckLocation;
}


function registerId(experiment){
  // posts a blank text file to server as a way of recording IDs who at least started the experiment

  var curId = (IsOnTurk())? GetAssignmentId() : prompt("Doesn't look like you are on Turk, so you are probably testing." + 
      "Enter an ID to save your data with:", "id");

  var dataToServer = {
    'curId': curId,
    'experiment': experiment,
    'sessionCode': 'init',
    'currentData': 'Worker ID: ' + GetWorkerId()
  }

  $.post(
    url = '../../../../../cgi-bin/saveData.py',
    data = dataToServer
    )
}




