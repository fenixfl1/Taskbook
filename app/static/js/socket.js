$(document).ready(function() {
	var socket = io.connect('http://' + document.domain + ':' + document.port + '/test');

	socket.on('my response', function(msg) {
		$('#test').append('<p> Recibed:' + msg.data + '</p>');
	});

	$('form#emit').submit(function (e) {
		socket.emit('my event', {data: $('#emit_data').val()});
        return false;
	});

	$('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });
});