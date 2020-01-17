<?php
	function xor_encrypt($in, $key) {
    	$text = $in;
    	$outText = '';

    	for($i=0;$i<strlen($text);$i++) {
    		$outText .= $text[$i] ^ $key[$i % strlen($key)];
    	}

    	return $outText;
	}

	$defaults = json_encode(array("showpassword"=>"no", "bgcolor"=>"#ffffff"));
	$secret = base64_decode("ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw=");

	$my_key = xor_encrypt($secret, $defaults);
	var_dump($my_key);
	$my_key = "qw8J";
	$my_array = json_encode(array("showpassword"=>"yes", "bgcolor"=>"#ffff22"));
	$my_cookie = xor_encrypt($my_array, $my_key);
	var_dump($my_cookie);
	$encoded_cookie = base64_encode($my_cookie);
	var_dump($encoded_cookie);
?>