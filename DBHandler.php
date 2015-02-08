<?php

class DBHandler {
	
	private $conn;

	public function __construct(){
		$this->conn = new mysqli("localhost", "root", "root", "droplet");
	}

	public function executeQuery($query){
		if (!$res = $this->conn->query($query)){
			echo "<br>Error: " . $query . "<br>" . $this->conn->error;
			return;
		}

		return $res;
	}

	public function insertAccessToken($phoneNumber, $accessToken){
		echo "here";
		$stmt = 
			"INSERT INTO droplet.tokens(phoneNumber, accessToken)
			VALUES ('$phoneNumber', '$accessToken');";

		return $this->executeQuery($stmt);
	}




}









?>