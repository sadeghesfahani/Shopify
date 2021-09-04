const fNameField = document.getElementById('id_lname')
const lNameField = document.getElementById('id_lname')
const email = document.getElementById('id_email')
const password = document.getElementById('id_password')
const submitButton = document.getElementById('submit')
const url = document.getElementById('id_url').value
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
email.addEventListener('change', handleChange);


async function handleChange() {
    const option = prepareOption()
    const response = await fetch(url,option)
    const data = await response.json()
    alert(data['server_response'])
}

function prepareOption(){
    const option = {
        method: 'POST',
        body : prepareData(),
        headers: prepareHeaders(),
    }
    return option

}

function prepareData() {
    const data = JSON.stringify({'username': email.value})
    return data
}
function prepareHeaders(){
    const  header = new Headers()
    header.append('X-CSRFToken', csrf)
    return header
}