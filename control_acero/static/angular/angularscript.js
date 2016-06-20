var controlacero = angular.module('controlacero', []);
	controlacero.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});
controlacero.controller('formatosController', ['$scope',function($scope) {
    $scope.miles = function(value) {
        console.log(value);
    };
	      //var textInputElement = document.getElementById('textInput');
	      //textInputElement.addEventListener('keyup', function(){
	        //console.log(this.value);
	      //});
}]);