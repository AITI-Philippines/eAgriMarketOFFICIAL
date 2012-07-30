
	$(function() {
		var availableTags = [
			"Brown Sugar",
			"White Sugar",
			"Sugar",
			"Rice",
			"White Rice",
			"Red Rice",
			"Japanese Rice",
			"Sticky Rice",
			"Flour",
			"Baking Powder",
			"Tilapia",
			"Bangus",
			"Fish",
			"Calamansi",
			"White Eggs",
			"Brown Eggs",
			"Eggs",
			"Coffee",
			"Dairy Milk",
			"Milk",
			"Soya Milk", 
			"Laman ng Tao" 
		];
		$( "#tags" ).autocomplete({
			source: function(request, response) {
				var results = $.ui.autocomplete.filter(availableTags, request.term);
        			response(results.slice(0, 5));
			}
			
			
		});
	});	
