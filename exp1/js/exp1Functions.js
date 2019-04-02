function findPercentile(trialArray, percentile){
	// takes as input the entire trialStruct and the desired percentile
	// returns the value in the RT distribution that aligns with the specified percentile
	// note; this doesn't perfectly align with the default mode of R's quantile() function, but i'm realizing there are many ways to calculate quartiles, so i think this way is fine
	// just in case of error, im setting the defaults as 50% = 679, and 35% = 562 (calculated from the overall rt distribution from foraging MTurk rvts)

	// some minimum number of trials that need to be present in order for these calculations to make sense
	
	var rtDist = [];
	var nTrials = trialArray.length;

	// in case this computation fails, make sure the scripts defaults on reasonable values
	var trialMin = 10;
	var windowMin = 350;

	for (i = 0; i < nTrials; i++){
		// only keep trials where rt < 1
		if (trialArray[i]['rt'] < 1000) {
			rtDist.push(trialArray[i]['rt']);
		}
	}


	// sort in ascending order
	rtDist = rtDist.sort(function(x, y){return x-y});

	// find position 
	var position = (percentile / 100) * nTrials;

	// control for whether position is a whole number
	if (position % 1) {
		position = Math.ceil(position);
		var value = rtDist[position - 1]
	}	else {
		var value = (rtDist[position - 1] + rtDist[position]) / 2
	}

	if (rtDist.length > trialMin && value > windowMin) {

		return value;

	} else {
		if (percentile > 40) {
			return 679;
		} else {
			return 562;
		}
	}


}

// for displaying points
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


// specific to deck prac 

function findTargetDeck(trialCount, deckCode) {
  
  var target = '';

  
  if (deckCode['left']['id'] == 'easy') {
    target = trialCount <= 10? 'left' : 'right';
  } else if (deckCode['right']['id'] == 'easy') {
    target = trialCount <= 10? 'right' : 'left';
  }
  
  return target;
}

function rtPercentilesToNumber(rtPercentiles){
  // takes as input the rtPercentiles dict
  // converts the values to numeric

  if (typeof(rtPercentiles['fiftieth']) == 'string') {
    rtPercentiles['fiftieth'] = parseInt(rtPercentiles['fiftieth']);
    rtPercentiles['thirtyFifth'] = parseInt(rtPercentiles['thirtyFifth']);
  }

  return rtPercentiles;

}

function calibrateDeckPoints(deckCode, pointCalibration, trialCount){
	// takes as inputs two dicts:
		// deckCode: {'left': {'id': 'hard', 'pSwitch': 0.8}, 'right': etc}
		// pointCalibration, keys: ['lowRewardPoints', 'highRewardPoints', 'currentAdjustment', 'prevDeckDifficulty']
	// updates both dicts as a return


	if (trialCount != 1) {
		if (pointCalibration['prevDeckDifficulty'] == 'hard') {
			pointCalibration['highRewardPoints'] = pointCalibration['highRewardPoints'] - pointCalibration['currentAdjustment'];
		} else {
			pointCalibration['highRewardPoints'] = pointCalibration['highRewardPoints'] + pointCalibration['currentAdjustment'];
		}

		pointCalibration['currentAdjustment'] = pointCalibration['currentAdjustment'] / 2

	}

	deckCode['left']['points'] = deckCode['left']['id'] == 'hard'? pointCalibration['highRewardPoints'] : pointCalibration['lowRewardPoints'];
	deckCode['right']['points'] = deckCode['right']['id'] == 'hard'? pointCalibration['highRewardPoints'] : pointCalibration['lowRewardPoints'];

	return [deckCode, pointCalibration];

}

function getCondition(phase){
  // takes in what phase it is
  // returns the condition

  var condition = '';

  if (phase == 'twoChoice'){
    if (Math.random() < .5) {
      condition = 'decoyAbsent';
    } else {
      condition = 'filler';
    }
    // this needs to randomly select between FOUR conditions
  } else if (phase == 'threeChoice') {
    var randy = Math.random();
    if (randy < .25) {
      condition = 'nearHighDemand';
    } else if (randy >= .25 && randy <= .5) {
      condition = 'nearLowDemand';
    } else if (randy > .5 && randy <= .75) {
      condition = 'filler';
    } else if (randy > .75) {
      condition = 'neutral';
    }
  }

  return condition;

}


function getDeckCode(nDecks, phase, condition, highRewardPoints) {
  // takes as input how many decks are in the array (only dealing with 2 for now)
  // and the phase ['prac']
  // returns a dict where the key is each spatial potision and values are specific to the decks

  var deckCode = {};
  var deckOne = {};
  var deckTwo = {};
  var deckThree = {}
  var varScale = 3;
  // compute random adjustments once and use throughout all ddecks
  var switchAdjustment = Math.round(rnorm() * varScale) / 100;
  var pointsAdjustment = Math.round(rnorm() * varScale);

  // run for everything except condition filler
  if (condition != 'filler') {
    deckOne['id'] = 'hard'
    deckOne['pSwitch'] = 0.8;
    deckTwo['pSwitch'] = 0.2;
    deckTwo['id'] = 'easy';

    // run for two and three choice phases
    if (phase != 'prac') {
      deckOne['pSwitch'] = deckOne['pSwitch'] + switchAdjustment;
      deckTwo['pSwitch'] = deckTwo['pSwitch'] + switchAdjustment;
      deckOne['points'] = highRewardPoints + pointsAdjustment;
      deckTwo['points'] = 50 + pointsAdjustment;
      
      // only run for three choice phase
      if (phase == 'threeChoice') {
        if (condition != 'neutral') {
          deckThree['id'] = condition == 'nearHighDemand'? 'decoyNearHard' : 'decoyNearEasy';
          deckThree['pSwitch'] = condition == 'nearHighDemand'? 0.84 : 0.2;
          deckThree['pSwitch'] = deckThree['pSwitch'] + switchAdjustment;
          deckThree['points'] = condition == 'nearHighDemand'? highRewardPoints : 48;
          deckThree['points'] = deckThree['points'] + pointsAdjustment;
        
        // if condition is neutral
        } else {
          deckThree['id'] = 'neutral';
          // needs to have a min of p(sw | hard deck) and max of .9
          // look in journal for logic of below line (p. 29 in journal)
          deckThree['pSwitch'] = (Math.random() * (.9 - deckOne['pSwitch'])) + deckOne['pSwitch'];
          // min of 0, max of points for low reward deck (~ 50)
          deckThree['points'] = (Math.random() * deckTwo['points'])
        }
      }
    }
    // if condition is filler
  } else {
    deckOne['id'] = 'filler';
    deckTwo['id'] = 'filler';
    deckThree['id'] = 'filler';
    deckOne['pSwitch'] = Math.random();
    deckTwo['pSwitch'] = Math.random();
    deckThree['pSwitch'] = Math.random();
    deckOne['points'] = Math.floor(Math.random() * highRewardPoints);
    deckTwo['points'] = Math.floor(Math.random() * highRewardPoints);
    deckThree['points'] = Math.floor(Math.random() * highRewardPoints);
  }

  deckCode = getDeckLocation(deckOne, deckTwo, deckThree, nDecks);

  
  return deckCode;
}