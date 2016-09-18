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

  $scope.sortKey = 'hotness_score';


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

    $scope.processTopic = function(topic, articles) {
        // We pick information from articles in some order
        var fields = ['video_url', 'image_url', 'date', 'image_url', 'summary', 'title'];

        for (var i = 0; i < articles.length; i++) {
            var article = articles[i];
            fields.map(function(field) {
                if (field in article) {
                    topic[field] = article[field]
                }
            });
        }
        topic.articles = articles;

        return topic;
    };

    $scope.populateFeed = function(response) {
        $scope.feed=[];
        $scope.shownFeed=[];
        console.log(response.length);
        for(i=0; i<response.length; i++) {
            topic = response[i];
            $scope.feed.push($scope.processTopic(topic[0], topic[1]));
        }

        // Sort the feed
        $scope.feed.sort(function(a, b) {
            keyA = a[$scope.sortKey],
            keyB = b[$scope.sortKey];

            if (keyA == null || keyA == '') {
                return 1;
            }

            if (keyB == null || keyB == '') {
                return -1;
            }

            if ($scope.sortKey == 'date') {
                keyA = new Date(keyA);
                keyB = new Date(keyB);
            }

            // Compare the 2 dates
            if(keyA < keyB) return 1;
            if(keyA > keyB) return -1;

            return 0;
        });

        limit = Math.min(10, $scope.feed.length);
        counter = 0;

        while(counter < limit) {
            $scope.shownFeed.push($scope.feed[counter]);
            counter++;
        }

        $scope.count = counter;
        $scope.$apply();
  };

    $scope.httpGetAsync = function() {
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





