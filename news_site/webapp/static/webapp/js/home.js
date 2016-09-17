var myApp = angular.module('newsApp', ['infinite-scroll']);

myApp.controller('HomeController', ['$scope', function($scope) {
  $scope.loginstatus = 'notloggedin';
  $scope.username = '';
  $scope.user = {
  	username: "",
  	password: ""
  };
  $scope.feed = [{title: "1", snippet: "1"}, {title: "2", snippet: "2"}, {title: "3", snippet: "3"}, {title: "4", snippet: "4"}];
  $scope.count = 5;


  $scope.login = function() {
  	$scope.loginstatus='successfullogin'; //TODO: implement (or not)
  	if($scope.user.username !== "") {
  		$scope.welcome = 'Welcome, ' + $scope.user.username + '!';
  	} else {
  		$scope.welcome = "?";
  	}
  	$('#myModal').modal('toggle');
  };

  $scope.loadMore = function() {
    //make api call to load more
    newScope = $scope.count+100;
    while($scope.count <= newScope) {
    	$scope.feed.push({title:$scope.count, snippet:$scope.count});
    	$scope.count++;
    }

  };
}]);