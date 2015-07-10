// Author is Fredrik A. Madsen-Malmo

$('tr').hide() // For cool transitions later

function getOnline () {
	// Gets the online status with a simple ajax request
	$('.entry').each(function (index, element) {
		$.ajax({
			type: 'POST',
			url: $(element).data('url'),
			timeout: 300000, // 5 minutes timeout
			error: function (x, t, m) {
				// If the error is a timeout (which is 5 minutes)
		        if (t === "timeout") {
		        	// Get the online-showing part of the entry
					var onlineChild = $(element).find('.online');

					$(element).fadeOut(1000);

					// Set the data-online attribute to False
					$(onlineChild).data('online', 'False');

					$(onlineChild).text('Offline').fadeIn(1000);

					$(onlineChild).css('color', '#c0392b');
		        }
		    },

		    // See above
		    success: function (data) {
		    	var onlineChild = $(element).find('.online');

				$(onlineChild).data('online', data);

			    $(onlineChild).fadeOut(1000, function () {
			    	if ($(onlineChild).data('online') == 'True') {
			    		$(onlineChild).css('color', '#27ae60');
						$(onlineChild).text('Online').fadeIn(1000);

						if ($(element).css('display') == 'none') {
							$(element).fadeIn(1000);
						}
					} else {
						$(onlineChild).text('Offline').fadeIn(1000);

						$(element).fadeOut(1000);

						$(onlineChild).css('color', '#c0392b');
					}
			    });
		    }
		});
	});
}

function showOffline () {
	$('.entry').each(function (index, element) {
		if ($(element).css('display') == 'none') {
			$(element).fadeIn(1000);
		}
	});

	$('#show').hide();
	$('#hide').show();
}

function hideOffline () {
	$('.entry').each(function (index, element) {
		if ($(element).find('.online').text() == 'Offline') {
			$(element).fadeOut(1000);
		}
	});

	$('#show').show();
	$('#hide').hide();

}

// Click on the refresh icon
$('#refresh').on('click', function (e) {
	// Don't redirect
	e.preventDefault()

	// For each of the Online-status <td>-s
	$('.online').each(function (index, element) {
		$(element).fadeOut(1000, function () {
			$(element).text('Refreshing..');
			$(element).css('color', '#7f8c8d');
			$(element).fadeIn(1000);
		});
	});

	// Update the status on all nodes
	getOnline();
});

$('#show').on('click', function () {
	showOffline();
});

$('#hide').on('click', function () {
	hideOffline();
});

// When everything is done loading
$(window).load(function () {
	$('tr').each(function (i,e) {
	  $(e).fadeIn(500 + i*200);
	});

	getOnline();

	// Fades away each panel after 1 second + 1 second for each panel
	$('.panel').each(function (index, element) {
		setTimeout(function () { $(element).fadeOut() }, 2000 + parseInt(index) * 1000)
	});
});