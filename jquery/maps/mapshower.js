  var geocoder;
  var map;
  var counter = 1;
  function hide(){
  
  }
  function initialize() {
   $('#map_canvas').hide();
   $('#show_map').removeAttr('disabled');
   var latlng = new google.maps.LatLng(16.4167, 120.6000);
    
    var mapOptions = {
      zoom: 12,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
  }
  
  function showMap(){
   
   if (counter == 1){
     $('#map_canvas').show('slow', function() {
      $('#show_map').attr('value','Hide Map');
   
     //  $("#map_canvas").animate({width:530},"slow");
    // Animation complete.
    google.maps.event.trigger(map,'resize');
  });
  	counter = 0;
  } else if (counter == 0){
   $('#map_canvas').hide()
   $('#show_map').attr('value','Show Map');
  counter = 1;
  }

   }
 
  
