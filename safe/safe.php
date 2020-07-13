<?php
error_reporting(E_ALL); //E_ALL

function cache_shutdown_error() {

    $_error = error_get_last();

    if ($_error && in_array($_error['type'], array(1, 4, 16, 64, 256, 4096, E_ALL))) {

        echo 'Runtime Error：</br>';
        echo 'Error:' . $_error['message'] . '</br>';
        echo 'File:' . $_error['file'] . '</br>';
        echo 'Line:' . $_error['line'] . '</br>';

    }
}

register_shutdown_function("cache_shutdown_error");

$arr = explode(PHP_EOL,file_get_contents(__DIR__."/whitelist"));

array_pop($arr);

if ( !in_array($_SERVER["SCRIPT_NAME"],$arr) ){
    header('HTTP/1.1 403 Forbidden');
    exit();
}
