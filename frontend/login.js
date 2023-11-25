import { url, EPsignup, EPlogin } from "./endpoints.js";
import { dashboardL } from "./locations.js"


const wrapper = document.querySelector('.wrapper');
const registerLink = document.querySelector('.register-link');
const loginLink = document.querySelector('.login-link');

registerLink.onclick = () => {
    wrapper.classList.add('active');
}

loginLink.onclick = () => {
    wrapper.classList.remove('active');
}

// function getData()
// {
//     //gettting the values
//     var signupusername= document.getElementById("signupusername").value; 
//     var signupemail = document.getElementById("signupemail").value;
//     var signuppassword= document.getElementById("signuppassword").value; 
//     //saving the values in local storage
//     localStorage.setItem("signupusername", susername);  
//     localStorage.setItem("signupemail", semail);
//     localStorage.setItem("signuppassword", spassword); 
//     console.log(localStorage.getItem(susername));
//     localStorage.setItem('test','test1');
// }

// const form = document.getElementById('signup-form');
// const signupusername = document.getElementById('signupusername');
// const signupemail = document.getElementById('signupemail');

// form.addEventListener('submit', function(e){
//     e.preventDefault();

//     const signupusernameValue = signupusername.value;
//     const signupemailValue = signupemail.value;

//     localStorage.setItem('signupusername', signupusernameValue);
//     localStorage.setItem('signupemail', signupemailValue);

//     window.location.href="uploadimage.html";
// })

const loginform = document.getElementById('login-form')
const signupform = document.getElementById('signup-form')

loginform.addEventListener("submit", (e) => {
    e.preventDefault()

    const inputs = loginform.elements;
    const userinfo = {
        username: inputs["username"].value,
        password: inputs["password"].value,
    };

    const form = new FormData(loginform)

    let asyncLogin = fetch(url + EPlogin, {
        method: "POST",
        body: form,

    })

    asyncLogin.then(
        (res) => {
            return res.json();
        }
    ).then((data) => {
        localStorage.setItem("token", data);
        window.location.href = dashboardL;
    })

    asyncLogin.catch(
        (res) => {
            alert("login failed");
        }
    )
});

signupform.addEventListener("submit", (e) => {
    e.preventDefault()

    const inputs = signupform.elements;
    const userinfo = {
        username: inputs["username"].value,
        password: inputs["password"].value,
        email: inputs["email"].value,
    };

    let asyncSignup = fetch(url + EPlogin, {
        method: "POST",
        headers: {

        },
        body: signupform,

    })

    asyncSignup.then(
        (res) => {
            localStorage.setItem("jwt-token", res.body)
            window.location.href = dashboardL;
        }
    )

    asyncSignup.catch(
        (res) => {
            alert("login failed");
        }
    )
});