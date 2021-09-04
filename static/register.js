const fNameField = document.getElementById('id_fname')
const lNameField = document.getElementById('id_lname')
const email = document.getElementById('id_email')
const password = document.getElementById('id_password')
const submitButton = document.getElementById('submit')
const check_username_url = document.getElementById('id_check_username_url').value
const register_url = document.getElementById('id_register_url').value
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
email.addEventListener('change', handleChange);
submitButton.addEventListener('click', (event) => handleRegister(event))


async function handleRegister(e) {
    e.preventDefault()
    const option = prepareOption()
    const response = await fetch(register_url, option)
    const data = await response.json()
    // alert(data['server_response'])

}

async function handleChange() {
    const option = prepareOption()
    const response = await fetch(check_username_url, option)
    const data = await response.json()
}

function prepareOption() {
    const option = {
        method: 'POST',
        body: prepareData(),
        headers: prepareHeaders(),
    }
    return option

}

function prepareData() {
    const data = JSON.stringify({
        'email': email.value,
        'fname': fNameField.value,
        'lname': lNameField.value,
        'password': password.value
    })
    return data
}

function prepareHeaders() {
    const header = new Headers()
    header.append('X-CSRFToken', csrf)
    return header
}
