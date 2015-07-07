// Author is Fredrik A. Madsen-Malmo

$(window).load(function() {
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

	$('.panel').each(function(index, element) {
		setTimeout(function() { $(element).fadeOut() }, 2000 + parseInt(index) * 1000)
	});
});