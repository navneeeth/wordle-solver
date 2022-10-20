var navLinks = document.getElementById('navLinks');
var current_guess = 1;
var word_entered = false;
var guessesArray = [];
var yellowSet = [];
var greenSet = [];
var blackSet = [];
var incorrectSet = [];
var correctSet = [];
var firstTime = true;
var incorrectList = [[], [], [], [], []];
var copyOfIncorrectList;
var correctList = [1, 1, 1, 1, 1];

function makeAnAPICall(wordInput) {
  var copyOfIncorrectSet = incorrectSet;
  console.log('copy:');
  console.log(JSON.stringify(copyOfIncorrectSet));
  /*
  for(var i = 0; i < 5; i++) {
    if(copyOfIncorrectSet[i] == null) {
      copyOfIncorrectSet[i] = '[]';
    }
  }
  */
  //console.log(JSON.stringify(copyOfIncorrectSet));
  console.log('IN the function.');
  const http = new XMLHttpRequest();
  var response = '';
  var status = 0;
  const params = {
    "first-guess": "["+guessesArray+"]",
    "yellow-set": "["+yellowSet+"]",
    "green-set": "["+greenSet+"]",
    "black-set": "["+blackSet+"]",
    "correct_set": "["+correctSet+"]",
    "incorrect_set": "["+copyOfIncorrectSet+"]",
    "guess-number": current_guess.toString()
  }

  console.log("Parameters:");
  //console.log(params);
  /*
  const params = {
    "first-guess": "['ADIEU', 'BACKS', 'SLASH', 'SMALL', 'SPALL']",
   "yellow-set": "[[1,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0],[0,0,0,0,0], [0,0,0,0,0]]",
   "green-set": "[[0,0,0,0,0],[0,0,0,0,0],[1,0,1,0,0],[1,0,1,1,1],[1,0,1,1,1]]",
   "black-set": "[[0,1,1,1,1],[1,0,1,1,0],[0,0,0,0,1],[0,1,0,0,0],[0,1,0,0,0]]",
   "correct_set": "[[1,1,1,1,1],[1,1,1,1,1],['S',1,'A',1,1],['S',1,'A','L','L'],['S',1,'A','L','L']]",
   "incorrect_set": "[[['A'],[],[],[],[]], [['A'],['A'],[],[],['S']], [['A'],['A', 'L'],[],[],['S']], [['A'],['A', 'L'],[],[],['S']], [['A'],['A', 'L'],[],[],['S']]]",
   "guess-number": "1"
  }

  "first-guess": "['ADIEU', 'BACKS', 'SLASH', 'SMALL', 'SPALL']",
 "yellow-set": "[[1,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0],[0,0,0,0,0], [0,0,0,0,0]]",
 "green-set": "[[0,0,0,0,0],[0,0,0,0,0],[1,0,1,0,0],[1,0,1,1,1],[1,0,1,1,1]]",
 "black-set": "[[0,1,1,1,1],[1,0,1,1,0],[0,0,0,0,1],[0,1,0,0,0],[0,1,0,0,0]]",
 "correct_set": "[[1,1,1,1,1],[1,1,1,1,1],['S',1,'A',1,1],['S',1,'A','L','L'],['S',1,'A','L','L']]",
 "incorrect_set": "[[['A'],[],[],[],[]], [['A'],['A'],[],[],['S']], [['A'],['A', 'L'],[],[],['S']], [['A'],['A', 'L'],[],[],['S']], [['A'],['A', 'L'],[],[],['S']]]",
 "guess-number": "3"
  */
  //http.open('POST', 'https://say-flight-backend.herokuapp.com/sign-up')
  http.open('POST', 'http://127.0.0.1:5000/first-guess');
  http.setRequestHeader('Content-type', 'application/json');
  console.log("Sent");
  console.log(JSON.stringify(params));
  http.send(JSON.stringify(params)); // Make sure to stringify
  //http.send();
  http.onload = function() {
      // Do whatever with response
      console.log('xhttp');
      console.log('Received');
      //console.log(http.responseText);
      var response = JSON.parse(http.responseText);
      var result = response.message;
      processedWords = result.processedWords;
      console.log(processedWords);
      var currRank = 1;
      for(var i = 1; i < 11; i++) {
        var wordSelector = 'tw'+ i;
        var probSelector = 'tp' + i;
        var word = document.getElementById(wordSelector);
        var prob = document.getElementById(probSelector);
        word.innerHTML = '';
        prob.innerHTML = '';
      }
      for(var i = 0; i < processedWords.length; i++) {
        console.log("Word:");
        console.log(processedWords[i][0]);
        console.log("Percentage:");
        console.log(processedWords[i][1]);
        var probNum = parseFloat(processedWords[i][1]);
        probNum = probNum * 100.0;
        probNum = probNum.toFixed(2);
        if(currRank > 10) {
          break;
        }
        var wordSelector = 'tw'+ currRank;
        var probSelector = 'tp' + currRank;
        var word = document.getElementById(wordSelector);
        var prob = document.getElementById(probSelector);
        word.innerHTML = processedWords[i][0].toUpperCase();
        prob.innerHTML = probNum+'%';
        currRank++;
      }
      /*
      response = JSON.parse(http.responseText);
      if(response.status == 'success') {
      console.log('Received');
        console.log(response.message);
        login_stat.innerHTML = '<p>You have successfully signed up! Login with your credentials.</p>'
        status = 1;
      }
      else {
        if(response.status=='401') {
          console.log("failure");

          //signup_stat.innerHTML = "<p style=\"color:Tomato;\">The email you entered is already in use. Please use another email.</p>";
          status = 0;
        }
        else {
          console.log("failure");

          //signup_stat.innerHTML = "<p style=\"color:Tomato;\">There is some error in the server. Please try again.</p>";
          status = 0;
        }

  }
    */
      }
      http.onerror = function() {
        console.log("failure");

        //signup_stat.innerHTML = "<p style=\"color:Tomato;\">There is some error in the server. Please try again.</p>";
        status = 0;
      }
}


function showMenu() {
    navLinks.style.right = "0";

}
    function hideMenu() {
        navLinks.style.right = "-200px";
    }
function isFiveLetters(wordInput) {

    if(wordInput.length != 5) {
        return false;
    }
    else {
      return true;
    }
}

function updateSpanText() {
  var span_text = document.getElementById('current_guess_span_two');
  switch(current_guess) {
    case 1:
      span_text.innerHTML = 'second';
      break;

    case 2:
      span_text.innerHTML = 'third';
      break;
    case 3:
      span_text.innerHTML = 'fourth';
      break;
    case 4:
     span_text.innerHTML = 'fifth';
     break;
    case 5:
    span_text.innerHTML = 'sixth';
    break;
    default:
      span_text.innerHTML = '0';
  }
}
function updateDisplay(wordInput) {
  var current_row = '.row'+current_guess;


  var span_text = document.getElementById('current_guess_span');
  switch(current_guess) {
    case 1:
      span_text.innerHTML = 'second';
      break;

    case 2:
      span_text.innerHTML = 'third';
      break;
    case 3:
      span_text.innerHTML = 'fourth';
      break;
    case 4:
     span_text.innerHTML = 'fifth';
     break;
    case 5:
    span_text.innerHTML = 'sixth';
    break;
    default:
      span_text.innerHTML = '0';
  }
  console.log(current_row);
  var row_entries = document.querySelectorAll(current_row);
  console.log(row_entries);
console.log(row_entries.length);
row_entries.forEach(row => {
  console.log(row.innerHTML);
  console.log(row);
  row.style.backgroundColor = '#777';
});
var first_letter_id = 'r' + current_guess + 'w1';
var second_letter_id = 'r' + current_guess + 'w2';
var third_letter_id = 'r' + current_guess + 'w3';
var fourth_letter_id = 'r' + current_guess + 'w4';
var fifth_letter_id = 'r' + current_guess + 'w5';
console.log(first_letter_id);
var first_letter = document.getElementById(first_letter_id);
var second_letter = document.getElementById(second_letter_id);
var third_letter = document.getElementById(third_letter_id);
var fourth_letter = document.getElementById(fourth_letter_id);
var fifth_letter = document.getElementById(fifth_letter_id);
first_letter.innerHTML = wordInput[0].toUpperCase();
second_letter.innerHTML = wordInput[1].toUpperCase();
third_letter.innerHTML = wordInput[2].toUpperCase();
fourth_letter.innerHTML = wordInput[3].toUpperCase();
fifth_letter.innerHTML = wordInput[4].toUpperCase();

}

function validateWord() {
  var wordInput = document.getElementById('word_input').value;
  wordInput = wordInput.replace(/\s+/g, ' ').trim();
  if (isFiveLetters(wordInput)) {
    updateDisplay(wordInput);
    //alert('Great!');
    word_entered = true;
    var guessSection = document.getElementById('guessProcess');
    var boxesSection = document.getElementById('enterBoxes');
    guessSection.style.visibility="hidden";
    boxesSection.style.visibility="visible";
  }
  else {
    alert('Enter a five-letter word.')
  }
}



function validateBoxes() {
// Function to check if all of the colours are updated
var wordInput = document.getElementById('word_input').value;
wordInput = wordInput.replace(/\s+/g, ' ').trim();
var first_letter_id = 'r' + current_guess + 'w1';
var second_letter_id = 'r' + current_guess + 'w2';
var third_letter_id = 'r' + current_guess + 'w3';
var fourth_letter_id = 'r' + current_guess + 'w4';
var fifth_letter_id = 'r' + current_guess + 'w5';
console.log(first_letter_id);
var first_letter = document.getElementById(first_letter_id);
var second_letter = document.getElementById(second_letter_id);
var third_letter = document.getElementById(third_letter_id);
var fourth_letter = document.getElementById(fourth_letter_id);
var fifth_letter = document.getElementById(fifth_letter_id);
first_letter_style = first_letter.style.backgroundColor;
second_letter_style = second_letter.style.backgroundColor;
third_letter_style = third_letter.style.backgroundColor;
fourth_letter_style = fourth_letter.style.backgroundColor;
fifth_letter_style = fifth_letter.style.backgroundColor;
var coloursArray = [first_letter_style, second_letter_style, third_letter_style, fourth_letter_style, fifth_letter_style];

if(first_letter_style != '' && second_letter_style != '' && third_letter_style != '' && fourth_letter_style != '' && fifth_letter_style != '') {
  console.log('Valid entry');
  updateSpanText();

  //alert('Great!');
  guessesArray.push('\''+wordInput+'\'');
  yellowList = [];
  greenList = [];
  blackList = [];
  console.log('Incorrect List');
  console.log(JSON.stringify(incorrectList));
  console.log('Correct List');
  console.log(correctList);
  for(var i = 0; i < 5; i++) {
    //yellow
    if(coloursArray[i] == 'rgb(245, 245, 54)') {
        yellowList.push(1);
        greenList.push(0);
        blackList.push(0);
        if(/[a-zA-Z]/.test(incorrectList[i]) == false) {
          console.log('Yellow letter new for');
          var letter = '\''+wordInput[i]+'\'';
          console.log('letter');
          console.log(letter);
          incorrectList[i] = [];
          incorrectList[i].push('\''+wordInput[i]+'\'');
        }
        else {
          var letter = '\''+wordInput[i]+'\'';
          console.log('letter');
          console.log(letter);
          console.log(incorrectList[i]);
          if(incorrectList[i].includes(letter) == false) {
            console.log("problem starts");
            var currentEntry = incorrectList[i];
            currentEntry = currentEntry.substr(0,currentEntry.length-2);
            currentEntry = currentEntry + '\', ' + letter + ']';
            console.log(currentEntry);
            incorrectList[i] = currentEntry;
            // incorrectList[i].push('\''+wordInput[i]+'\'');
          }
        }

    }
    //green
    else if(coloursArray[i] == 'rgb(24, 163, 52)') {
      yellowList.push(0);
      greenList.push(1);
      blackList.push(0);
      if(correctList[i] == '1') {
        correctList[i] = '\''+wordInput[i]+'\'';
      }
    }
    else {
      yellowList.push(0);
      greenList.push(0);
      blackList.push(1);
    }
  }

  copyOfIncorrectList = incorrectList;
  console.log('copy of incorrect list now:');
  console.log(JSON.stringify(copyOfIncorrectList));
  for(var i = 0; i < 5; i++) {
    console.log('Currently at i = '+i);
    console.log(copyOfIncorrectList[i]);
    if(copyOfIncorrectList[i].length == 0 || copyOfIncorrectList[i] == '[]') {
      copyOfIncorrectList[i] = '[]';
    }
    else {
      if(copyOfIncorrectList[i].includes('[') == false) {
        copyOfIncorrectList[i] = '[' + copyOfIncorrectList[i] + ']';
      }
    }
  }
  firstTime = false;
  console.log('after op');
  console.log(JSON.stringify(copyOfIncorrectList));

  yellowSet.push('['+yellowList+']');
  greenSet.push('['+greenList+']');
  blackSet.push('['+blackList+']');
  incorrectSet.push('['+copyOfIncorrectList+']');
  correctSet.push('['+correctList+']');
  //yellowSet.push();
  makeAnAPICall(wordInput);
  current_guess++;
  word_entered = false;
  var guessSection = document.getElementById('guessProcess');
  var boxesSection = document.getElementById('enterBoxes');
  guessSection.style.visibility="visible";
  boxesSection.style.visibility="hidden";
}
else {
  alert('Finish choosing the colours!');
}
}



function letterClick(letter_id) {
  console.log(letter_id);
  letter_dom = document.getElementById(letter_id);
  current_style = letter_dom.style.backgroundColor;
  console.log(current_style);
  //grey
  if(current_style == 'rgb(119, 119, 119)') {
    letter_dom.style.backgroundColor = '#18a334';
  }
  //green
  else if(current_style == 'rgb(24, 163, 52)') {
    letter_dom.style.backgroundColor = '#f5f536';
  }
  //yellow
  else if(current_style == 'rgb(245, 245, 54)') {
    letter_dom.style.backgroundColor = '#777';
  }
  else {
    console.log('current guess:');
    console.log(current_guess.toString());
    console.log('current row:');
    console.log(letter_id[1]);
    if(current_guess.toString() == letter_id[1] && word_entered == true) {
      letter_dom.style.backgroundColor = '#18a334';
    }
  }
}
