var myApp = angular.module('newsApp', ['infinite-scroll']);

myApp.controller('HomeController', ['$scope', function($scope) {
  $scope.loginstatus = 'notloggedin';
  $scope.username = '';
  $scope.showDetails = true;
  $scope.user = {
  	username: "",
  	password: ""
  };
  var title = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi auctor.";
  var snippet = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer sagittis est nec accumsan auctor. Aliquam sollicitudin mollis mi vel pretium. Praesent tellus risus, pulvinar nec commodo eu, egestas eu purus. Nulla feugiat, dui nec tristique ornare, nunc lectus auctor libero, venenatis tincidunt nunc nibh at elit. Donec eu congue ligula, et tincidunt arcu. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla porta lobortis suscipit. Aliquam sed eros quis enim blandit vehicula. Integer ac nulla non massa vehicula pulvinar. Aenean varius nisi non odio ultricies, sit amet iaculis nisi porta.";
  $scope.feed = [
    [{title: "1"+title, snippet: "1"+snippet},
    {title: "2"+title, snippet: "2"+snippet},
    {title: "3"+title, snippet: "3"+snippet},
    {title: "4"+title, snippet: "4"+snippet}]];
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
    newScope = $scope.count+40;
    temp = []
    while($scope.count <= newScope) {
    	temp.push({title:$scope.count+title, snippet:$scope.count+snippet});
    	$scope.count++;
    }
    $scope.feed.push(temp);

  };
}]);