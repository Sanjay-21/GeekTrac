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

const form = document.getElementById('form1');
const signupusername = document.getElementById('signupusername');
const signupemail = document.getElementById('signupemail');

form.addEventListener('submit', function(e){
    e.preventDefault();

    const signupusernameValue = signupusername.value;
    const signupemailValue = signupemail.value;

    localStorage.setItem('signupusername', signupusernameValue);
    localStorage.setItem('signupemail', signupemailValue);

    window.location.href="uploadimage.html";
})