var myApp = angular.module('newsApp', ['infinite-scroll']);

myApp.controller('HomeController', ['$scope', function($scope) {
  $scope.loginstatus = 'notloggedin';
  $scope.username = '';
  $scope.showDetails = true;
  $scope.user = {
  	username: "",
  	password: ""
  };
  $scope.feed = [];
  $scope.shownFeed = [];
  $scope.count = 1;


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
    if($scope.count<=$scope.feed.length){
      $scope.shownFeed.push($scope.feed[$scope.count]);
      $scope.count++;
    }
  };

  $scope.populateFeed = function(response) {
    console.log(response);
    response = JSON.parse(response);
    console.log(response);
    console.log(response.length);
    for(i=0; i<response.length; i++) {
      topic = response[i];
      topicDetails = topic[0] //where to store this?
      articles = topic[1]
      console.log("articles length " + articles.length);
      $scope.feed.push(articles);
    }
    if($scope.feed.length > 0) {
      $scope.shownFeed.push($scope.feed[0]);
      $scope.$apply();
    }

  };

  $scope.httpGetAsync = function() {
        $scope.feed=[];
        $scope.shownFeed=[];
        url = window.location+"api/v1/articles";
        callback = $scope.populateFeed;
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                callback(xmlHttp.responseText);
        }
        xmlHttp.open("GET", url, true); // true for asynchronous 
        categories = [];
        $('.categories li input:checkbox:checked').each(function () {
          console.log("hi");
          var sThisVal = (this.checked ? $(this).val() : null);
          if(sThisVal) {
            categories.push(sThisVal);
          }
        });
        console.log(categories);
        sources = [];
        $('.sources li input:checkbox:checked').each(function () {
          console.log("hi");
          var sThisVal = (this.checked ? $(this).val() : null);
          if(sThisVal) {
            sources.push(sThisVal);
          }
        });
        console.log(sources);
        xmlHttp.send(JSON.stringify(categories), JSON.stringify(sources));
  };

  $(document).ready(function() {
    $scope.httpGetAsync();
  });

}]);





