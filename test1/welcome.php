<html>
	<head>
	  <meta charset="UTF-8">
	  <title>Pre Sing Up</title>
	  <meta name="YOB" content="width=device-width, initial-scale=1">
	  <link href="_/CSS/sign_up_page.css" rel="stylesheet">
	  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	  <link href="_/CSS/diseno.css" rel="stylesheet">

	</head>

	<body>

	<div class="topnav" id="myTopnav">
	  <a>YOB</a>
	  <a href="index.html">YOB</a>
	  <a href="#Pro Tips">Pro Tips</a>
	  <a href="#Contacto">Contacto</a>
	</div>

	HV <?php echo $_POST["hv"]; ?><br>
	Oferta <?php echo $_POST["oferta"]; ?><br>


	<div style="background-color:black;color:white;text-align:center;margin-left: 33%;margin-right: 33%; margin-top: 15%;margin-bottom:15%">
		  <h2>Regístrate o accede a tu cuenta para desbloquear todas las posiblidas de conseguir empleo.</h2>
			<h3>Es así de sencillo!</h3>
				<!-- Button to open the modal -->
			<button onclick="document.getElementById('id01').style.display='block'">Sign Up</button> 
			<!-- Button to open the modal login form -->
			<button onclick="document.getElementById('id02').style.display='block'">Login</button>
	</div>



<!-- The Modal (contains the Sign Up form) -->
<div id="id01" class="modal">
  <span onclick="document.getElementById('id01').style.display='none'" class="close" title="Close Modal">&times;</span>
  <form class="modal-content animate" action="/action_page.php">
    <div class="container">
      <label><b>Email</b></label>
      <input type="text" placeholder="Enter Email" name="email" required>

      <label><b>Password</b></label>
      <input type="password" placeholder="Enter Password" name="psw" required>

      <label><b>Repeat Password</b></label>
      <input type="password" placeholder="Repeat Password" name="psw-repeat" required>
      <input type="checkbox" checked="checked"> Remember me
      <p>By creating an account you agree to our <a href="#">Terms & Privacy</a>.</p>

      <div class="clearfix">
        <button type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelbtn">Cancel</button>
        <button type="submit" class="signupbtn1">Sign Up</button>
      </div>
    </div>
  </form>
</div>


<!-- The Modal -->
<div id="id02" class="modal">
  <span onclick="document.getElementById('id02').style.display='none'" 
	class="close" title="Close Modal">&times;</span>

  <!-- Modal Content -->
  <form class="modal-content animate" action="/action_page.php">

    <div class="container">
      <label><b>Username</b></label>
      <input type="text" placeholder="Enter Username" name="uname" required>

      <label><b>Password</b></label>
      <input type="password" placeholder="Enter Password" name="psw" required>

      <button type="submit">Login</button>
      <input type="checkbox" checked="checked"> Remember me
    </div>

    <div class="container" style="background-color:#f1f1f1">
      <button type="button" onclick="document.getElementById('id02').style.display='none'" class="cancelbtn">Cancel</button>
      <span class="psw">Forgot <a href="#">password?</a></span>
    </div>
  </form>
</div>
	

	</body>
</html>