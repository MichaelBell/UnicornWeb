'use strict';


var app = angular.module('app', ['teTouchevents']).

  factory('socket', function ($rootScope) {
    console.log("socket factory");
    var socket = new WebSocket("ws://" + location.host + "/ws");
    return {
      send: function(msg) {
        socket.send(msg);
      },
      onmessage: function(callback) {
        socket.onmessage = callback;
      },
      close: function() { socket.close(); }
    }
  });

