var myApp = angular.module('newsApp', ['infinite-scroll']);

myApp.controller('HomeController', ['$scope', function($scope) {
  $scope.loginstatus = false;

  var lastUser = sessionStorage.getItem('lastUser')
  if (lastUser == null) {
    $scope.loginstatus = false;
    $scope.user = {
      username: "",
      password: ""
    };
  } else {
    $scope.user = {'username': lastUser}
    loginSetUp();
  }
  $scope.showDetails = true;
  
  $scope.feed = [];
  $scope.shownFeed = [];
  $scope.count = 1;

  $scope.sortKey = 'hotness_score';
  $scope.sourceMap = {
    'cnn': 'CNN',
    'yahoo': 'Yahoo',
    'washingtonpost': 'Washington Post',
    'huffingtonpost': 'Huffington Post',
    'theguardian': 'The Guardian',
    'wsj': 'WSJ',
    'dailymail': 'Daily Mail',
    'nytimes': 'NY Times',
    'foxnews': 'Fox News',
    'nbcnews': 'NBC News'
  };

  $scope.login = function() { // This is like when you actually click the log in button and log in
  	loginSetUp(); 
    setPreferences();
    $scope.httpGetAsync();
  	$('#myModal').modal('toggle');
  };

  function loginSetUp() { 
    $scope.loginstatus=true; //TODO: implement (or not)
    if($scope.user.username !== "" && $scope.user.password !== "") {
      $scope.welcome = 'Welcome, ' + $scope.user.username + '!';
      $('.user-features').css('display', 'block');
    }

    sessionStorage.setItem('lastUser', $scope.user.username);
  };

  function setPreferences() {
    var username = $scope.user.username;
    if (sessionStorage.getItem(username + '-categories') != null) {

      var cats = sessionStorage.getItem(username + '-categories').split(',');
      $('.categories li input:checkbox').each(function () {
        if (!cats.includes($(this).val())) {
          this.checked = false;
        } else {
          this.checked = true;
        }
      });
    }

    if(sessionStorage.getItem(username + '-sources') != null) {
      var sos = sessionStorage.getItem(username + '-sources').split(',');
      $('.sources li input:checkbox').each(function () {
        if (!sos.includes($(this).val())) {
          this.checked = false;
        } else {
          this.checked = true;
        }
      });
    }

    if (sessionStorage.getItem(username + '-sortKey') == 'hotness_score') {
      $('#hotness-radio').prop('checked', true);
    } else {
      $('#date-radio').prop('checked', true);
    }
  };

  $scope.loadMore = function() {
    if($scope.count<=$scope.feed.length){
      $scope.shownFeed.push($scope.feed[$scope.count]);
      $scope.count++;
    }
  };

  $scope.loadSummary = function(index, topic) {
    
    topic.summary = topic.articles[index].summary;
    topic.summarylink = topic.articles[index].article_url;
  };

  $scope.selectedVal = function(name){
    $scope.$parent.val = name;
  };
  function getCategories() {
    var categories = [];
    $('.categories li input:checkbox:checked').each(function () {
      console.log("hi");
      var sThisVal = (this.checked ? $(this).val() : null);
      if(sThisVal) {
        categories.push(sThisVal);
      }
    });
    return categories
  };

  function getSources() {
    var sources = [];
    $('.sources li input:checkbox:checked').each(function () {
      console.log("hi");
      var sThisVal = (this.checked ? $(this).val() : null);
      if(sThisVal) {
        sources.push(sThisVal);
      }
    });
    return sources;
  };

    $scope.processTopic = function(topic, articles) {
        // We pick information from articles in some order
        var fields = ['video_url', 'image_url', 'date', 'image_url', 'summary', 'title']; //two image_urls?

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
        var categories = getCategories();
        sessionStorage.setItem($scope.user.username + '-categories', categories);
        var sources = getSources();
        sessionStorage.setItem($scope.user.username + '-sources', sources);
        sessionStorage.setItem($scope.user.username + '-sortKey', $scope.sortKey);

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
    setPreferences();
    $scope.httpGetAsync();
  });

}]);





