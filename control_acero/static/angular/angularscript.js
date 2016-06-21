var controlacero = angular.module('controlacero', []);
	controlacero.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});
controlacero.controller('formatosController', ['$scope',function($scope) {
    $scope.miles = function(value) {
	    var x = value.split('.');
	    var x1 = x[0];
	    var x2 = x.length > 1 ? '.' + x[1] : '';
	    var rgx = /(\d+)(\d{3})/;
	    while (rgx.test(x1)) {
	        x1 = x1.replace(rgx, '$1' + ',' + '$2');
	    }
	    $scope.textModel = "";
        console.log(x1 + x2);
    };
}]);