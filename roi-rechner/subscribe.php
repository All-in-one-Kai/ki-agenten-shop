<?php
// CULA-125: Brevo contact subscription proxy
// Forwards form submissions to Brevo via Maton gateway (server-side token).
// Expected POST JSON: {"email":"...","firstname":"..."}

header("Content-Type: application/json");

// Only allow POST from same site or our domain
$origin = $_SERVER["HTTP_ORIGIN"] ?? "";
$referer = $_SERVER["HTTP_REFERER"] ?? "";
$allowed = ["ki-agenten.shop", "www.ki-agenten.shop"];
$host = parse_url($referer, PHP_URL_HOST);

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["error" => "Method not allowed"]);
    exit;
}

if (!empty($origin)) {
    $originHost = parse_url($origin, PHP_URL_HOST);
    if (!in_array($originHost, $allowed, true)) {
        http_response_code(403);
        echo json_encode(["error" => "Forbidden"]);
        exit;
    }
}

$raw = file_get_contents("php://input");
$data = json_decode($raw, true);

$email = trim($data["email"] ?? "");
$firstname = trim($data["firstname"] ?? "");

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(["error" => "Invalid email"]);
    exit;
}

$maton_token = "MtbKXzwUfngtHSU7hrRqe87MW5w7NfMN0VinlegCO6t4K_zIYJOE6Jc-iAUdNshJE8u27x_2aZUFCGNn4Lkdj3nLgsZgdSrUzKM";
$brevo_list_id = 5;

$payload = [
    "email" => $email,
    "listIds" => [$brevo_list_id],
    "updateEnabled" => true,
    "attributes" => [],
];
if ($firstname !== "") {
    $payload["attributes"]["FIRSTNAME"] = $firstname;
}

$ch = curl_init("https://gateway.maton.ai/brevo/v3/contacts");
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($payload),
    CURLOPT_HTTPHEADER => [
        "Authorization: Bearer $maton_token",
        "Content-Type: application/json",
        "Accept: application/json",
    ],
    CURLOPT_TIMEOUT => 10,
]);

$response = curl_exec($ch);
$status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Brevo returns 201 on create, 204 on update (contact already exists)
if ($status === 201 || $status === 204 || $status === 200) {
    http_response_code(200);
    echo json_encode(["ok" => true]);
} else {
    http_response_code(502);
    echo json_encode(["error" => "Upstream error", "status" => $status]);
}
