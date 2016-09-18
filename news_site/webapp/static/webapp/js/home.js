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
    if($scope.count<=$scope.feed.length){
      $scope.shownFeed.push($scope.feed[$scope.count]);
      $scope.count++;
    }
  };

  $scope.populateFeed = function(response) {
    console.log(response.length);
    for(i=0; i<response.length; i++) {
      topic = response[i];
      topicDetails = topic[0] //where to store this?
      articles = topic[1]
      console.log("articles length " + articles.length);
      $scope.feed.push(articles);
    }
    limit = Math.min(10, $scope.feed.length);
    counter = 0;
    while(counter<limit) {
      $scope.shownFeed.push($scope.feed[counter]);
      counter++;
    }
    $scope.count = counter;
    $scope.$apply();

  };

    $scope.httpGetAsync = function() {
        $scope.feed=[];
        $scope.shownFeed=[];

        var categories = [];
        $('.categories li input:checkbox:checked').each(function () {
          console.log("hi");
          var sThisVal = (this.checked ? $(this).val() : null);
          if(sThisVal) {
            categories.push(sThisVal);
          }
        });

        var sources = [];
        $('.sources li input:checkbox:checked').each(function () {
          console.log("hi");
          var sThisVal = (this.checked ? $(this).val() : null);
          if(sThisVal) {
            sources.push(sThisVal);
          }
        });

        url = "api/v1/articles/";
        $.ajax({
            url: url,
            data: {
                categories: JSON.stringify(categories),
                sources: JSON.stringify(sources),
            },
            success: function(response) {
                $scope.populateFeed(response);
            },
        });
    };

  $(document).ready(function() {
    $scope.httpGetAsync();
  });

}]);





