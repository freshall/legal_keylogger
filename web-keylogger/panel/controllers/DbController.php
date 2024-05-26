<?php
$dbHOST = "localhost";
$dbUSER = "root";
$dbPASS = "root";
$dbNAME = "keylogger";
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

@$db = mysqli_connect($dbHOST, $dbUSER, $dbPASS, $dbNAME);

if (!$db) {
    echo 'DataBase connection error';
    exit();
}

mysqli_set_charset($db, 'utf8');
