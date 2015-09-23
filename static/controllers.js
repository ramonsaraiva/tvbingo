'use strict';

var controllers = angular.module('controllers', []);

controllers.controller('bingo_controller', ['$scope', '$location', '$http', function($scope, $location, $http) {
	$scope.players = 4;
	$scope.match = null;

	$scope.create = function()
	{
		$http.post('/matches/', {'players': $scope.players})
			.success(function(data) {
				$scope.match = data;
			})
			.error(function(e) {
				alert('error');
			});
	}
}]);
