let tokenURL = "http://127.0.0.1:9000/api/users/token/"

let form = document.getElementById('login--form')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let formData = {
        'username': form.username.value,
        'password': form.password.value
    }
    console.log(formData)

    fetch(tokenURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            console.log('DATA', data)
            if(data.access){
                localStorage.setItem('token', data.access)
                window.location = 'file:///C:/Users/bsnag/Documents/Django/Frontend/projects-list.html'
            }
            else{
                alert('Username or Password didnt work')
            }
        })
})