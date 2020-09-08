
function my_reset() {
    let form = document.getElementById("login-form");
    console.log(form);
    form.submit();
    form.reset();
    form.value = "";
}