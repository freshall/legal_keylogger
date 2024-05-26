<?php

function encryptRequest($input)
{
   $key = 'ztWuu0JVnaFm0rtDi1qd6Fwlus61MOkv';
   $inputLen = strlen($input);
   $keyLen = strlen($key);

   if ($inputLen <= $keyLen) {
      return $input ^ $key;
   }

   for ($i = 0; $i < $inputLen; ++$i) {
      $input[$i] = $input[$i] ^ $key[$i % $keyLen];
   }
   return $input;
}

function fix_string($string)
{
   global $db;

   $string = htmlspecialchars(mysqli_escape_string($db, $string));

   return $string;
}

function getUserName($username)
{
   global $db;

   $user = fix_string($username);

   $query = "SELECT * FROM `users` WHERE `username` = '{$user}'";

   $result = mysqli_query($db, $query);
   $userinfo = mysqli_fetch_assoc($result);

   if ($userinfo != null) {
      return $user;
   }
   if ($userinfo == null) {
      return false;
   }
}

function getUserPassword($password)
{
   global $db;

   $pass = fix_string($password);

   $query = "SELECT * FROM `users` WHERE `password` = '{$pass}'";

   $result = mysqli_query($db, $query);
   $passinfo = mysqli_fetch_assoc($result);

   if ($passinfo != null) {
      return $pass;
   }
   if ($passinfo == null) {
      return false;
   }
}

function getUserInfo($username)
{
   global $db;

   $user = fix_string($username);

   $query = "SELECT * FROM `users` WHERE `username` = '{$user}'";

   $result = mysqli_query($db, $query);
   $userinfo = mysqli_fetch_assoc($result);

   return $userinfo;
}

function setIp($username)
{
   global $db;

   $user = fix_string($username);
   $ip = $_SERVER['REMOTE_ADDR'];

   $query = "UPDATE `users` SET `ip` = '{$ip}' WHERE `username` = '{$user}'";
   mysqli_query($db, $query);
}

function setActive($username, $active)
{
   global $db;

   $user = fix_string($username);

   $query = "UPDATE `users` SET `active` = '{$active}' WHERE `username` = '{$user}'";
   mysqli_query($db, $query);
}

function createNewLog($username, $application, $application_title, $event_log)
{
   global $db;

   $date = date("Y-m-d H:i:s");
   $username_sec = fix_string($username);
   $application_sec = fix_string($application);
   $application_title_sec = fix_string($application_title);
   $event_log_sec = fix_string($event_log);
   $event_log_sec_json = json_encode($event_log_sec, JSON_UNESCAPED_UNICODE);

   $query = "INSERT INTO `logs` (`username`, `application`, `application_title`, `event_log`, `created_at`) VALUES ('{$username_sec}', '{$application_sec}', '{$application_title_sec}', '{$event_log_sec_json}', '{$date}')";

   return mysqli_query($db, $query);
}



function getAllLogs($username)
{
   global $db;
   
   $user = fix_string($username);
   $query = "SELECT * FROM `logs` WHERE `username` = '{$user}'";

   $result = mysqli_query($db, $query);

   while ($row = mysqli_fetch_assoc($result)) {
      $array[] = $row;
   }
   return $array;
}

function getAllUsers()
{
   global $db;
   
   $query = "SELECT * FROM `users`";

   $result = mysqli_query($db, $query);

   while ($row = mysqli_fetch_assoc($result)) {
      $array[] = $row;
   }
   return $array;
}