'use strict';

var controllers = angular.module('controllers', []);

controllers.controller('bingo_controller', ['$scope', '$location', '$http', '$timeout', function($scope, $location, $http, $timeout) {
	$scope.players = 4;
	$scope.match = null;
	$scope.cards = [];
	$scope.waiting = ['.', '..', '...'];
	$scope.waiting_i = -1;
	var check_timer;
	var waiting_dots_timer;

	$scope.create = function()
	{
		$http.post('/matches/', {'players': $scope.players})
			.success(function(data) {
				$scope.match = data;
				check_match();
				waiting_dots();
			})
			.error(function(e) {
				alert('error');
			});
	}

	$scope.join = function()
	{
		$http.post('/matches/cards/', {'code': $scope.code})
			.success(function(data) {
				$scope.cards.push(data);
			})
			.error(function(e) {
				alert('error');
			});
	}

	$scope.start = function()
	{
		if ($scope.match.ready)
		{
			$timeout.cancel(check_timer);
			$timeout.cancel(waiting_dots_timer);
		}
		else
		{
			alert('Still waiting for all players..');
		}
	}

	function waiting_dots() {
		$scope.waiting_i = ($scope.waiting_i + 1) % 3;
		waiting_dots_timer = $timeout(waiting_dots, 250);
	}

	function check_match() {
		$http.get('/matches/' + $scope.match.id + '/')
			.success(function(data) {
				$scope.match = data;
				console.log($scope.match);
				check_timer = $timeout(check_match, 2000);
			})
			.error(function(e) {
				alert('error');
			});
	}
}]);
