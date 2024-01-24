document.getElementById("password").addEventListener("input", function () {
  var password = this.value;
  var passwordStrength = document.getElementById("passwordStrength");
  var passwordHelp = document.getElementById("passwordHelp");
  var registerBtn = document.getElementById("registerBtn");

  passwordStrength.style.width = "0%";
  passwordStrength.classList.remove("bg-danger", "bg-warning", "bg-success");
  passwordHelp.textContent = "";

  var conditions = [/[A-Z]/, /[a-z]/, /\d/, /[#!?@$%^&*-]/];

  var fulfilledConditions = conditions.reduce(function (count, condition) {
    return count + condition.test(password);
  }, 0);

  var strength = (fulfilledConditions / conditions.length) * 100;

  if (strength < 50) {
    passwordStrength.classList.add("bg-danger");
    passwordHelp.textContent = "Weak password";
    registerBtn.disabled = true;
  } else if (strength < 80) {
    passwordStrength.classList.add("bg-warning");
    passwordHelp.textContent = "Medium strength password";
    registerBtn.disabled = true;
  } else {
    passwordStrength.classList.add("bg-success");
    passwordHelp.textContent = "Strong password";
    registerBtn.disabled = false;
  }

  passwordStrength.style.width = strength + "%";
});

document
  .getElementById("confirm_password")
  .addEventListener("input", function () {
    var password = document.getElementById("password").value;
    var confirm_password = this.value;
    var registerBtn = document.getElementById("registerBtn");

    if (password === confirm_password) {
      this.setCustomValidity("");
      registerBtn.disabled = false;
    } else {
      this.setCustomValidity("Passwords do not match");
      registerBtn.disabled = true;
    }
  });
