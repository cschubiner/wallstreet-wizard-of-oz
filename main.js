var
  questions = require('./lib/cli'),
  Q = require('q'),
  _ = require('underscore'),
  shell = require('shelljs'),
  quotes = require('./lib/quotes'),
  git = require('./lib/git'),
  chalk = require('chalk');

function runCommand(cmd) {
  return shell.exec(cmd).code === 0;
}

a = console.log;
var spaces = '     ';

function logGreen(str) {
  console.log(chalk.green(str));
}

function logYellow(str) {
  console.log(chalk.yellow(str));
}

function recommendCommand(cmd, cannotRun) {
  logGreen('clay recommends that you run the following command:');
  logYellow(spaces + cmd);
  a();

  if (cannotRun) {
    return;
  }

  var mainOptions = {
    PROCEED: 'Yes',
    QUIT: 'No'
  };
  var mainQuestionId = 'mainChoice';
  var mainQuestion = 'do you want clay to do it for you?';

  return questions.misc.arbitraryList(
    mainQuestionId,
    mainQuestion,
    _.values(mainOptions)
  ).then(function (answer) {
    switch (answer[mainQuestionId]) {
    case mainOptions.PROCEED:
      return runCommand(cmd);
    case mainOptions.QUIT:
      break;
    }
  });
}

function gRep(str, repWhat, repWith) {
  return str.replace(new RegExp(repWhat.source, 'g'), repWith);
}

function mainMenu() {

  var currentBranch = git.getCurrentBranchName();
  var mainOptions = {
    CHECKOUT: 'Checkout a new branch using JIRA',
    CHECKOUT_EXISTING: 'Checkout an existing branch',
    FETCH_REBASE: 'Fetch and rebase',
    PUSH_CURR: 'Push to origin/' + currentBranch,
    PUSH_MASTER: 'Push to origin/master',
    QUIT: 'Quit'
  };

  if (currentBranch === 'master') {
    delete mainOptions.PUSH_CURR;
  }

  var mainQuestionId = 'mainChoice';
  var mainQuestion = 'What do you want to do?';

  return questions.misc.arbitraryList(
    mainQuestionId,
    mainQuestion,
    _.values(mainOptions)
  ).then(function (answer) {
    switch (answer[mainQuestionId]) {
    case mainOptions.CHECKOUT:
      return checkoutBranch();
    case mainOptions.CHECKOUT_EXISTING:
      return checkoutExistingBranch();
    case mainOptions.PUSH_CURR:
      return pushToCurrentBranch(currentBranch);
    case mainOptions.FETCH_REBASE:
      return fetchAndRebase();
    case mainOptions.PUSH_MASTER:
      return pushToMasterBranch(currentBranch);
    case mainOptions.QUIT:
      break;
    }
  });
}

function main() {
  return mainMenu()
    .then(function (success) {
      console.log();
      console.log(quotes.getRandomInspiration());
      console.log();
      logGreen('Thanks for using clay!');
    })
    .fail(function (error) {
      console.log('Oops! Looks like there was an error.');
      console.log(error);
    });
}

main();
