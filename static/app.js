'use strict';

var app = angular.module('app', [
	'ngRoute',
	'monospaced.qrcode',
	'controllers',
	'services'
]);

app.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/bingo/', {
			templateUrl: 'partials/bingo.tpl.html'
		})
		.otherwise({
			redirectTo: '/bingo/'
		});
}]);
