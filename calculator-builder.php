<?php
/*
Plugin Name: Calculator Builder
Plugin URI: http://provideyourown.com
Description: Build your own custom calculators
Version: 0.1
Author: Scott Daniels
Author URI: http://provideyourown.com
License: GPL2
*/

/*
Using the calculator builder is quite simple:
1) You must define the calculator you want built by creating a MYCALCULATOR.txt file inside the calculators directory.
  In this file, you specify the various fields and equations. See filament.txt as an example.
2) In the cmd-line, run the python calculator 'compiler': $ python compile_calculator.py MYCALCULATOR
  Note: You do not need to specify either the director or the .txt extension, just the calculator name of which a file with the name + .txt exists
3) In the page where you want the calculator to appear, add this shortcode:  [calculator name="MYCALCULATOR"]
*/


add_shortcode( 'calculator', function ( $attr, $content = null ) {
  global $add_calculator_script;

  extract( shortcode_atts( array( 'name' => '' ), $attr ) );
  $add_calculator_script = $name;
  $dir = plugin_dir_path( __FILE__ ); // https://codex.wordpress.org/Function_Reference/plugin_dir_path
  $fname = realpath("$dir/calculators/$name.html");
  $html = file_get_contents($fname);
  //$fname = realpath(CHILDTHEMELIB . '/calculators/' . $name . '.js');
  //$js = file_get_contents($fname);

  return $html;
});


/*************** register calculator script ***************************/
// see - http://scribu.net/wordpress/optimal-script-loading.html

//define('CALCULATOR_DIR', 'calculators/');

// register script, but don't actually add it to the page unless it is used (See next func)
add_action('init', function () {
  $dir = plugin_dir_path( __FILE__ ); // https://codex.wordpress.org/Function_Reference/plugin_dir_path
  $files = glob($dir.'/calculators/*.js');
  foreach ($files as $script) {
    $name = basename($script, ".js");
    $url = plugins_url("calculators/$name.js" , __FILE__ ); // https://codex.wordpress.org/Function_Reference/plugins_url
    //echo "Registering Scripts: " . $name . "; path" . $script . "\n";
    wp_register_script('calculator-'.$name, $url, array('jquery'), '1.0', true);
  }
});


// actually add script to page if it is used (by setting the global add_calculator_script = true)
add_action('wp_footer', function () {
	global $add_calculator_script;

	if ( $add_calculator_script ) {
    echo "Printing script: ".$add_calculator_script."\n";
    wp_print_scripts('calculator-'.$add_calculator_script);
    //$fname = realpath(CHILDTHEMELIB . '/calculators/' . $add_calculator_script . '.js');
    //$js = file_get_contents($fname);
    //$src = get_stylesheet_directory_uri() . '/library/calculators/' . $add_calculator_script . '.js';
    //echo "<script type='text/javascript' src='" . $src . "'></script>\n";
    //echo "Done printing script\n";
  }
});
