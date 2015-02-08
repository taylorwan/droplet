<?php
	require_once "dropbox-sdk-php-1.1.4/lib/Dropbox/autoload.php";
	use \Dropbox as dbx;
	session_start(); ?>

<!DOCTYPE html>

<html>

<head>
<title>Droplet - OAuth 2.0</title>
	<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="style-main.css">
</head>

<body class="oauth">
	<aside class="sidenav">
		<a href="../index.html" class="logo">
			<span class="title">Droplet</span>
			<img src="droplet-logo.png" />
		</a>
		<ul class="links">
			<li><a href="../index.html">Home</a></li>
			<li><a href="../docs.html">Docs</a></li>
			<li><a href="#">Setup</a></li>
		</ul>
	</aside>
	<div class="container">
		<h1>Droplet - OAuth 2.0</h1>
		<p class="lead">An SMS interactive tool for Dropbox.</p>

		<?php

			$appInfo = dbx\AppInfo::loadFromJsonFile('credentials.json');
			$clientIdentifier = "Droplet/1.0";
			$redirectUri = "https://localhost/oauth2_pt2.php";
			$csrfTokenStore = new dbx\ArrayEntryStore($_SESSION, 'dropbox-auth-csrf-token');

			$webAuth = new dbx\WebAuthNoRedirect($appInfo, $clientIdentifier);

			$_SESSION['webAuth'] = $webAuth;

			$authorizeUrl = $webAuth->start();

			echo "<a style=\"color:#fff\" href=\"$authorizeUrl\">Click me to find your code!</a>";

			echo "
				<form method='POST' action='oauth2_pt2.php'>
					<input type='text' name='code' class='form-control' placeholder='code'></input>
					<input type='text' name='phoneNumber' class='form-control' placeholder='phone #'></input>
					<input type='submit'>
				</form>";
				


		?>
	</div>

</body>

</html>
