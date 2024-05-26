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
    
    //password and user exists -> let's to login
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
    {
        die();
    }

    if ($_POST["username"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    
    //password and user exists -> let's to login
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        $logsArray = getAllLogs($user);
        echo ($logsArray);
        if (is_array($logsArray)) foreach ($logsArray as $logs) 
        {
            echo (($logs['event_log'] . "\n"));
            //die();
    
        }
        //$array = array('Status' => 'Successful standart user');
        //echo encryptRequest(json_encode($array));
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo (json_encode($array));
        die();
    }
    else 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username error');
        echo encryptRequest(json_encode($array));
        die();
    }



    // $logsArray = getAllLogs();

    // if (is_array($logsArray)) foreach ($logsArray as $logs) 
    // {
    
    //     echo $logs['key'];
    
    // }



} else if ($_POST["method"] == "applicationlogs") 
{
    if (!isset($_POST["username"])) 
    {
        die();
    }

    if ($_POST["username"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    
    //password and user exists -> let's to login
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        $logsArray = getAllLogs($user);
        
        if (is_array($logsArray)) 
        {
            foreach ($logsArray as $logs) {
                $responseArray = array(); // nani ????????????
                $responseArray[] =  (array('created_at' => $logs['created_at'], 'application' => $logs['application'], 'application_title' => $logs['application_title']));
                //die();
            }
            echo json_encode($responseArray);
        }
    
        //$array = array('Status' => 'Successful standart user');
        //echo encryptRequest(json_encode($array));
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo (json_encode($array));
        die();
    }
    else 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username error');
        echo encryptRequest(json_encode($array));
        die();
    }



    // $logsArray = getAllLogs();

    // if (is_array($logsArray)) foreach ($logsArray as $logs) 
    // {
    
    //     echo $logs['key'];
    
    // }



} else if ($_POST["method"] == "allusers") 
{

    $usersArray = getAllUsers();
    if (is_array($usersArray)) 
    {
        foreach ($usersArray as $user) 
        {
            if ($user["admin"] == 0) {
                //echo $user['id'];
                //echo $user['username'];
                //echo encryptRequest(json_encode($user['username'])); //bug
			    echo (json_encode($user['username']));
                //die();
            }
        }
    }
} else if ($_POST["method"] == "getactive") 
{
    if (!isset($_POST["username"])) 
    {
        die();
    }

    if ($_POST["username"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    
    //password and user exists -> let's to login
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        
        echo (($userinfo['active']));
        //$array = array('Status' => 'Successful standart user');
        //echo encryptRequest(json_encode($array));
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo (json_encode($array));
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
    {
        die();
    }

    if ($_POST["username"] == "") 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is empty');
        echo encryptRequest(json_encode($array));
        die();
    }

    $user = getUserName($_POST["username"]);
    $userinfo = getUserInfo($user);
    
    
    //password and user exists -> let's to login
    if ($user == $_POST["username"] && $userinfo["admin"] == 0) 
    {
        
        setActive($_POST["username"], $_POST["active"]);
        //$array = array('Status' => 'Successful standart user');
        //echo encryptRequest(json_encode($array));
        die();
    }
    else if ($user == $_POST["username"] && $userinfo["admin"] == 1) 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username is admin');
        echo (json_encode($array));
        die();
    }
    else 
    {
        $array = array('Status' => 'Error', 'msg' => 'Username error');
        echo encryptRequest(json_encode($array));
        die();
    }
}

//TODO: if username == user -> nado fix
//TODO: Successful standart\admin user -> unsecure -> fix: make_token base64(sha256)