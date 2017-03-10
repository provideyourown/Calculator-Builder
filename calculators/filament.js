jQuery(document).ready(function($) {
  function calculate_length() {
    var density = parseFloat($("#density").val());
    var dia = parseFloat($("#dia").val());
    var weight = parseFloat($("#weight").val());
    var result =  weight / ( density * 3.14159 * dia * dia * 0.25 );
    $("#length").val(result.toFixed(2));
  }



  function calculate_weight() {
    var density = parseFloat($("#density").val());
    var dia = parseFloat($("#dia").val());
    var length = parseFloat($("#length").val());
    var result =  length * density * 3.14159 * dia * dia * 0.25;
    $("#weight").val(result.toFixed(2));
  }



  function calculate_volume() {
    var dia = parseFloat($("#dia").val());
    var length = parseFloat($("#length").val());
    var result =  length * 3.14159 * dia * dia * 0.25;
    $("#volume").html(result.toFixed(2));
  }



  function calculate_cost() {
    var weight = parseFloat($("#weight").val());
    var price = parseFloat($("#price").val());
    var result =  price * weight / 1000.0;
    $("#cost").html(result.toFixed(2));
  }



  $("#density").change(function () { 
calculate_length(); 
calculate_weight(); 
calculate_volume(); 
calculate_cost(); 

});

  $("#dia").change(function () { 
calculate_length(); 
calculate_weight(); 
calculate_volume(); 
calculate_cost(); 

});

  $("#length").change(function () { 
calculate_weight(); 
calculate_volume(); 
calculate_cost(); 

});

  $("#weight").change(function () { 
calculate_length(); 
calculate_volume(); 
calculate_cost(); 

});

  $("#volume").change(function () { 
calculate_length(); 
calculate_weight(); 
calculate_cost(); 

});

  $("#price").change(function () { 
calculate_length(); 
calculate_weight(); 
calculate_volume(); 
calculate_cost(); 

});

  $("#cost").change(function () { 
calculate_length(); 
calculate_weight(); 
calculate_volume(); 

});



});
