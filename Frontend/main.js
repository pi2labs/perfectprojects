
let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('Logout-btn')

let token = localStorage.getItem('token')

if(token){
    loginBtn.remove()
}
else{
    logoutBtn.remove()
}

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = 'file:///C:/Users/bsnag/Documents/Django/Frontend/login.html'
})

let projectsUrl = 'http://127.0.0.1:9000/api/projects'

let getProjects = () => {
    
    fetch(projectsUrl)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        buildProjects(data)
    })
}

let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById('projects--wrapper')
    projectsWrapper.innerHTML = ''
    
    for (let i = 0; projects.length > i; i++){
        let project = projects[i]
        
        let projectCard = `
            <div class='project--card'>
                <img src='http://127.0.0.1:9000${project.featured_image}'>
                <div>
                    <div class='card--header'>
                        <h3>${project.title}</h3>
                        <strong class='vote--option' data-vote='up' data-project="${project.id}">&#43;</strong>
                        <strong class='vote--option' data-vote='down' data-project="${project.id}">&#8722;</strong>
                    </div>
                    <i>${project.vote_ratio}% Positive Feedback</i>
                    <br>
                    <br>
                    <i>${project.vote_total} Vote</i>

                    <p>${project.description.substring(0, 150)}</p>
                </div>
            </div>
        `

        projectsWrapper.innerHTML += projectCard
    }

    // add listeners
    addVoteEvents()

}

let addVoteEvents = () => {
    let voteBtn = document.getElementsByClassName('vote--option')

    for (let i = 0; voteBtn.length > i; i++) {
        voteBtn[i].addEventListener('click', (e) => {
            let token = localStorage.getItem('token')
            
            let vote = e.target.dataset.vote
            let project = e.target.dataset.project

            fetch(`http://127.0.0.1:9000/api/projects/vote/${project}/`, {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({'value': vote}),
                
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success', data)
                getProjects()
            })
        })

    }
}
getProjects()
