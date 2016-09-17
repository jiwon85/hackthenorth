var myApp = angular.module('newsApp',[]);

myApp.controller('HomeController', ['$scope', function($scope) {
  $scope.loginstatus = 'notloggedin';
  $scope.username = '';
  $scope.user = {
  	username: "",
  	password: ""
  };

  $scope.login = function() {
  	$scope.loginstatus='successfullogin'; //TODO: implement (or not)
  	if($scope.user.username !== "") {
  		$scope.welcome = 'Welcome, ' + $scope.user.username + '!';
  	} else {
  		$scope.welcome = "?";
  	}
  	$('#myModal').modal('toggle');
  }
}]);