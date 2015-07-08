// Author is Fredrik A. Madsen-Malmo

$(window).load(function() {
	// Gets the online status with a simple ajax request
	$('.entry').each(function(index, element) {
		$.ajax({
			type: 'POST',
			url: $(element).data('url')
		}).done(function(data) {
			var onlineChild = $(element).find('.online');
			$(onlineChild).data('online', data);

		    $(onlineChild).fadeOut(1000, function() {
		    	if ($(onlineChild).data('online') == 'True') {
					$(onlineChild).text('Online').fadeIn(1000);;
				} else {
					$(onlineChild).text('Offline').fadeIn(1000);;
				}
		    });
		});
	});

	// Fades away each panel after 1 second + 1 second for each panel
	$('.panel').each(function(index, element) {
		setTimeout(function() { $(element).fadeOut() }, 2000 + parseInt(index) * 1000)
	});

	// This will post the user on the other peer collection website by 'bytecode'
	$('.submit_new').on('click', function() {
		$.ajax({
			type: 'POST',
			url: 'http://aether.mygen.ca/addpeer.php',
			data: {
				alias: $('#name').val(),
				address: $('#id').val(),
				port: $('#port').val()
			}
		});
	});
});