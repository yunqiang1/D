<?php

header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

$host = 'localhost';
$db   = 'yutu';
$user = 'root';
$pass = '123456';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
    $stmt = $pdo->query("SELECT * FROM recordings");
    $recordings = $stmt->fetchAll();

    // Process the file paths
    foreach ($recordings as &$recording) {
        // Replace the path prefix and backslashes
        $recording['file_path'] = str_replace("C:\\yutu\\dev\\", "../", $recording['file_path']);
        $recording['file_path'] = str_replace("\\", "/", $recording['file_path']);
    }

    echo json_encode($recordings);
} catch (\PDOException $e) {
    throw new \PDOException($e->getMessage(), (int)$e->getCode());
}

?>
