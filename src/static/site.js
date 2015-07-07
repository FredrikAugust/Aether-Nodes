// Author is Fredrik A. Madsen-Malmo

$(document).load(function() {
	$('.entry').each(function(index, element) {
		$.ajax({
			type: 'POST',
			url: $(element).data('url'),
			data: $(element).data('ip')
		}).done(function(data) {
			alert(data);
		});
	});

	$('.online').each(function(index, element) {
		if ($(element).data('online') == 'True') {
			$(element).text('Online');
		} else {
			$(element).text('Offline');
		}
	});
});