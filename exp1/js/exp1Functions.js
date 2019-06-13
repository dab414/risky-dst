function createConditionOrder() {
  // returns an array of four objects in random order
  // where each object represents a condition in format:
    // eg, {'name': 'HE', 'pSwitch': 0.9}

  var conditionHolder = [
    {
      'name': 'EM',
      'pSwitch': 0.3
    },

    {
      'name': 'EE',
      'pSwitch': 0.1
    },

    {
      'name': 'HM',
      'pSwitch': 0.7
    },

    {
      'name': 'HE',
      'pSwitch': 0.9
    }
  ];

  var conditionOrder = new Array();

  // following code from: https://stackoverflow.com/questions/12987719/javascript-how-to-randomly-sample-items-without-replacement
  // don't run more times than length of the object being indexed
  // not sure why this works tbh

  var n = conditionHolder.length;

  for (var i = 0; i < n; i++) {
    var randomIndex = Math.floor(Math.random() * conditionHolder.length);
    conditionOrder[i] = conditionHolder.splice(randomIndex, 1)[0];
  }

  return conditionOrder;
}



function createDeckCode(currentCondition) {
  // takes as input what the current condition is
    // comes in as an object: {'name': 'HE', 'pSwitch': 0.9}
  // builds up the pSwitch for decks, sends to getDeckLocation (globalFunctions.js) to assign locations
  // returns object: {'left': {'name': 'HE', 'pSwitch': 0.9}, 'right': {etc}}

  var deckOne = {};
  var deckTwo = {};

  deckOne = {'name': 'reference', 'pSwitch': 0.5};
  deckTwo = currentCondition;

  return getDeckLocation(deckOne, deckTwo, '', 2);

}