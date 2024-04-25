let video;
let canvas;
let nameInput;

function init() {
    //run web first time tehn webcam automatic
    video = document.getElementById("video")
    canvas = document.getElementById("canvas")
    nameInput = document.getElementById("name")

    //open webcam using navigator
    navigator.mediaDevices.getUserMedia({video:true})
        .then(stream=>{
            video.srcObject = stream
        })
        .catch(error=>{
            console.log("error access webcam", error)
        })
}
//create function to capture photo
function capture() {
    const context = canvas.getContext("2d")
    context.drawImage(video, 0, 0, canvas.width, canvas.height)
    canvas.style.display = "block"  //display
    video.style.display = "none"    //no display
}
//create register function
function register() {
    const name = nameInput.value
    const photo = dataURItoBlob(canvas.toDataURL())

    if(!name || !photo){
        alert("name and photo required please")
        return
    }
    const formData = new FormData()
    formData.append("name", name)
    formData.append("photo",photo,`${name}.jpg`)

    fetch("/register",{
        method:"POST",
        body: formData
    })
    .then(response=>response.json())
    .then(data=> {
        if(data.success){
            alert("Registration Successfull")
            // window.location.href= "/"  <- just reloading the page
            //TRYING TO DIRECT IT TO A NEW LOGIN PAGE (index2)
            window.location.href = "/index2"//?user_name" + nameInput.value
        }
        else{
            alert("Registration Failed!! Please try again.")
        }
    })
    .catch(error=>{
        console.log("error", error)
        alert("An error occurred. Please try again.")
    })
}

function login(){

    const context = canvas.getContext("2d")
    context.drawImage(video, 0, 0, canvas.width , canvas.height)
    const photo = dataURItoBlob(canvas.toDataURL())

    if(!photo){
        alert("photo required please")
        return 
    }
    const formData = new FormData()
    formData.append("photo", photo,"login.jpg")

    fetch("/login" , {
        method:"POST",
        body:formData
    })
    .then(response=>response.json())
    .then(data=>{
        console.log(data) // Add this line to see the actual response received from the server
        if(data.success){
            alert("Login successful!! Welcome, " + data.name)
            // and redirect to success.html
            window.location.href = '/success?user_name=' + data.name
        }
        else{
            alert("login failed, Please try again")
        }
        }).catch(error=>{
        console.log("error ", error)
        alert("An error occurred. Please try again.");
        })
}

function dataURItoBlob(dataURI){
    //to create a blob image from the captured image to compare the facial structure among the pictures
    //bytestring is save as data and mimestring for its datatype
    const byteString = atob(dataURI.split(",")[1]) 
    //atob decodes the bytestring into binary characters
    const mimeString = dataURI.split(",")[0].split(":")[1].split(":")[0]

    //arratBuffer is used to create a new blob object
    const ab = new ArrayBuffer(byteString.length) //for decoded binary strings
    const ia = new Uint8Array(ab)// for storing byte values

    //this loop iterates through the decoded binary string with its corresponding byte value and storing it in 'Uint8Array'
    for (let i = 0; i < byteString.length; i++){
        ia[i] = byteString.charCodeAt(i)
    }

    return new Blob([ab],{type:mimeString})
}

init()


