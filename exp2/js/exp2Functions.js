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

