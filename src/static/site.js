// Author is Fredrik A. Madsen-Malmo

$(document).load(function() {
	$('.entry').each(function(index, element) {
		$.ajax({
			type: 'POST',
			url: $(element).data('url')
		}).done(function(data) {
			var onlineChild = $(element).find('.online');
			$(onlineChild).data('online', data);

			if ($(onlineChild).data('online') == 'True') {
				$(onlineChild).text('Online');
			} else {
				$(onlineChild).text('Offline');
			}
		});
	});
});