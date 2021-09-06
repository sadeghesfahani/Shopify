const fNameField = document.getElementById('id_fname')
const lNameField = document.getElementById('id_lname')
const register_email = document.getElementById('id_email')
const register_password = document.getElementById('id_password')
const registerSubmitButton = document.getElementById('register_submit')
const loginSubmitButton = document.getElementById('login_submit')
const registerCsrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const loginCsrf = document.getElementsByName('csrfmiddlewaretoken')[1].value
const login_email = document.getElementById('id_login_email')
const login_password = document.getElementById('id_login_password')
window.addEventListener('DOMContentLoaded', fetchRequiredUrls)
register_email.addEventListener('change', handleChange);
registerSubmitButton.addEventListener('click', (event) => handleRegister(event))
loginSubmitButton.addEventListener('click', (event) => handleLogin(event))


async function fetchRequiredUrls() {
    const data = await fetch('http://127.0.0.1:8000/account/generalinfo')
    const urls = await data.json()
    window.urls = await urls
}

async function handleLogin(e) {
    e.preventDefault()
    const option = prepareLoginOption()
    const response = await fetch(window.urls['authentication'], option)
    const data = await response.json()
    alert(data['server_response'])
}

function prepareLoginOption() {
    const option = {
        method: 'POST',
        body: prepareLoginData(),
        headers: prepareLoginHeaders(),
    }
    return option

}

function prepareLoginData() {
    const data = JSON.stringify({
        'email': login_email.value,
        'password': login_password.value,
        'action': 'login',
    })
    return data
}

function prepareLoginHeaders() {
    const header = new Headers()
    header.append('X-CSRFToken', loginCsrf)
    return header
}

async function handleRegister(e) {
    e.preventDefault()
    const option = prepareRegisterOption()
    const response = await fetch(window.urls['authentication'], option)
    const data = await response.json()
    alert(data['server_response'])
}


function prepareRegisterOption() {
    const option = {
        method: 'POST',
        body: prepareRegisterData(),
        headers: prepareRegisterHeaders(),
    }
    return option

}

function prepareRegisterData() {
    const data = JSON.stringify({
        'email': register_email.value,
        'first_name': fNameField.value,
        'last_name': lNameField.value,
        'password': register_password.value,
        'action': 'register',
    })
    return data
}

function prepareRegisterHeaders() {
    const header = new Headers()
    header.append('X-CSRFToken', registerCsrf)
    return header
}

async function handleChange() {
        const response = await fetch(window.urls['checkuserexistance'] + '?email=' + register_email.value)
    const data = await response.json()
}

