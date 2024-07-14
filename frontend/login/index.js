const passwordInput = document.getElementById("password");
const urlParams = new URLSearchParams(window.location.search);
const loginPrompt = document.getElementById("login");

let thing = 0;

function wrongPass() {
    if (thing !== 0) return;
    thing++;
    const wrongPass = document.getElementById("wrong-password");
    wrongPass.innerText = "Wrong password, try again";
    loginPrompt.insertBefore(wrongPass, loginPrompt.children[1]);
}

function login() {
    const password = passwordInput.value;
    passwordInput.value = "";
    if(password === "") return;

    fetch("/verifylogin",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({password: password}),
        }
    ).then(response => {
        if (response.ok) {
            document.cookie = `password=${password}`;
            window.location.href = `${window.location.href}dashboard`;
        } else {
            wrongPass();
        }
    }).catch(err => console.error(err));
}