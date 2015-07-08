// Author is Fredrik A. Madsen-Malmo

$('tr').hide() // For cool transitions later

function getOnline() {
	// Gets the online status with a simple ajax request
	$('.entry').each(function(index, element) {
		$.ajax({
			type: 'POST',
			url: $(element).data('url'),
			timeout: 300000,
			error: function(x, t, m) {
		        if(t === "timeout") {
					var onlineChild = $(element).find('.online');
					$(onlineChild).data('online', 'False');

		            $(onlineChild).fadeOut(1000, function() {
						$(onlineChild).css('color', '#c0392b');
						$(onlineChild).text('Offline').fadeIn(1000);
					});
		        }
		    },
		    success: function(data) {
		    	var onlineChild = $(element).find('.online');
				$(onlineChild).data('online', data);

			    $(onlineChild).fadeOut(1000, function() {
			    	if ($(onlineChild).data('online') == 'True') {
			    		$(onlineChild).css('color', '#27ae60');
						$(onlineChild).text('Online').fadeIn(1000);
					} else {
						$(onlineChild).css('color', '#c0392b');
						$(onlineChild).text('Offline').fadeIn(1000);
					}
			    });
		    }
		});
	});
}

$(window).load(function() {
	$('tr').each(function(i,e) {
	  $(e).fadeIn(500 + i*200);
	});

	getOnline();

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

$('#refresh').on('click', function(e) {
	e.preventDefault()

	$('.online').each(function(index, element) {
		$(element).fadeOut(1000, function() {
			$(element).text('Refreshing..');
			$(element).css('color', '#7f8c8d');
			$(element).fadeIn(1000);
		});
	});

	getOnline();
});