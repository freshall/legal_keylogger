<?php
require '../controllers/DbController.php';
include '../controllers/UserController.php';

if (!isset($_POST["method"]))
    die();

if ($_POST["method"] == "auth") 
{
    if (!isset($_POST["username"]) || !isset($_POST["password"]))
        die();

    if ($_POST["username"] == "" || $_POST["password"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Enter the username and password');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $password = getUserPassword($_POST["password"]);
    $userinfo = getUserInfo($user);
    setIp($user);
    
    //password and user exists -> let's go to login
    if ($user == $_POST["username"] && $password == $_POST["password"] && $userinfo["admin"] == 0) 
    {
        $array = array('Status' => 'Successful standart user');
        echo encryptRequest(json_encode($array));
        die();
    }
    else if ($user == $_POST["username"] && $password == $_POST["password"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Successful admin user');
        echo encryptRequest(json_encode($array));
        die();
    }
    else {
        $array = array('Status' => 'Error', 'msg' => 'Incorrect username or password');
        echo encryptRequest(json_encode($array));
        die();
    }
} else if ($_POST["method"] == "logs") 
{
    if (!isset($_POST["username"])) 
        die();
    
    if ($_POST["username"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        $logsArray = getAllLogs($user);
        $logs = [];
        
        if (is_array($logsArray)) {
            foreach ($logsArray as $log) 
            {
                $logs[] = $log['event_log'];
            }
        }

        echo encryptRequest(implode("\n", $logs));
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo encryptRequest(json_encode($array));
        die();
    }
    else 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username error');
        echo encryptRequest(json_encode($array));
        die();
    }
} else if ($_POST["method"] == "getapplicationlogs") 
{
    if (!isset($_POST["username"])) 
        die();
    
    if ($_POST["username"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        $logsArray = getAllApplicationLogs($user);
        
        if (is_array($logsArray)) 
        {
            foreach ($logsArray as $logs) {
                $responseArray[] =  (array('last_press' => $logs['last_press'], 'application_exe' => $logs['application_exe'], 'application_title' => $logs['application_title']));
            }
            echo encryptRequest(json_encode($responseArray));
        }
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo encryptRequest(json_encode($array));
        die();
    }
    else 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username error');
        echo encryptRequest(json_encode($array));
        die();
    }
} else if ($_POST["method"] == "getapplicationlogsbyclick") 
{
    if (!isset($_POST["username"]) || !isset($_POST["application_exe"]))  
        die();
    
    if ($_POST["username"] == "" || $_POST["application_exe"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username or application is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        $logsArray = getApplicationLogs($user, $_POST["application_exe"], $_POST["application_title"]);
        
        if (is_array($logsArray)) 
        {
            foreach ($logsArray as $logs) 
            {
                $responseArray[] = (array('created_at' => $logs['created_at'], 'event_log' => $logs['event_log']));
            }
            echo encryptRequest(json_encode($responseArray));
        }
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo encryptRequest(json_encode($array));
        die();
    }
    else 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username error');
        echo encryptRequest(json_encode($array));
        die();
    }
} else if ($_POST["method"] == "allusers") 
{
    $usersArray = getAllUsers();
    $users = [];

    if (is_array($usersArray)) 
    {
        foreach ($usersArray as $user) 
        {
            if ($user["admin"] == 0) 
            {
                $users[] = $user['username'];
            }
        }
    }
    echo encryptRequest(implode("\n", $users));
    die();
    
} else if ($_POST["method"] == "getactive") 
{
    if (!isset($_POST["username"]))
        die();
    
    if ($_POST["username"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        echo encryptRequest($userinfo['active']);
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo encryptRequest(json_encode($array));
        die();
    }
    else 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username error');
        echo encryptRequest(json_encode($array));
        die();
    }
} else if ($_POST["method"] == "setactive") 
{
    if (!isset($_POST["username"]) || !isset($_POST["active"]))
        die();
    
    if ($_POST["username"] == "" || !isset($_POST["active"])) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username or active is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        setActive($_POST["username"], $_POST["active"]);
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo encryptRequest(json_encode($array));
        die();
    }
    else 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username error');
        echo encryptRequest(json_encode($array));
        die();
    }
}