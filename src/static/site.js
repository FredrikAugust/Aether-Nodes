// Author is Fredrik A. Madsen-Malmo

$('tr').hide() // For cool transitions later

var offline;

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

					// Set the data-online attribute to False
					$(onlineChild).data('online', 'False');

					// Self explanatory
		            $(onlineChild).fadeOut(1000, function() {
						$(onlineChild).css('color', '#c0392b');
						$(onlineChild).text('Offline').fadeIn(1000);
					});
		        }
		    },

		    // See above
		    success: function (data) {
		    	var onlineChild = $(element).find('.online');
				$(onlineChild).data('online', data);

			    $(onlineChild).fadeOut (1000, function () {
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

	// Hide offline nodes
	hideOffline();
}

function showOffline () {
	$(offline).each(function (index, element) {
		// Append one offline node after the last entry and then remove the node from the array
		$('.entry').last().after(offline.shift()).hide().fadeIn(100);
	});

	$('#show').show();
	$('#hide').hide();
}

function hideOffline () {
	offline = [];  // Clear the offline nodes list

	$('.online').each(function (index, element) {
		if ($(element).text() == 'Offline') {
			offline.push($(element).parent());
			$(element).parent().remove();
		}
	});

	$('#show').hide();
	$('#hide').show();
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

	// Show offline nodes
	showOffline();

	// Update the status on all nodes
	getOnline();

	// Hide offline nodes
	hideOffline();
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