var lastInstructionShowed = 1

let instructions = [
    "Escolha uma imagem de fundo:",
    "Escolha a imagem que você deseja camuflar:",
    "Posicione-a sobre o fundo:",
    "Aguarde um momento",
]

let extraHtml = [
    "<input id=\"background-input\" type=\"file\" onchange=\"didSelectBackground(this)\">",
    "<input id=\"overlay-input\" type=\"file\" onchange=\"didSelectOverlay(this)\">",
    "",
    ""
]

var background = undefined
var overlay = undefined

function didSelectBackground(input) {
    
    var reader = new FileReader();
    
    reader.onload = function(e) {
        
        if (lastInstructionShowed < 2) {
            addInstruction(2);
        }
        
        background = e.target.result
        updateImages();
    }
    
    reader.readAsDataURL(input.files[0]);
    
}

function didSelectOverlay(input) {
    
    var reader = new FileReader();
    
    reader.onload = function(e) {
        
        if (lastInstructionShowed < 3) {
            addInstruction(3);
        }
        
        overlay = e.target.result
        updateImages();
        
    }
    
    reader.readAsDataURL(input.files[0]);
    
}

function updateImages() {
    
    if (lastInstructionShowed >= 3) {
        
        img = document.getElementById('image')
        img.src = background;
        
        img.onload = function() {
            showResize(overlay, img.width, img.height);
        }
        
    }
        
}

function addInstruction(index) {
    
    if (index < instructions.length) {
        
        var newElement = document.createElement('p');
        newElement.innerHTML = "<b>" + index + ". </b>" + instructions[index - 1] + extraHtml[index - 1];
        
        let instructionsDiv = document.getElementById('instructions-div')
        instructionsDiv.appendChild(newElement);
        
    }

    if (lastInstructionShowed < index) {
        lastInstructionShowed = index;
    }
    
}

window.onload = function () {
    addInstruction(1);
}

// ========================================================================


function loadFile(o) {
    var fr = new FileReader();
    
    fr.onload = function(e) {
        var content = e.target.result
        
        // let BASE_URL = "https://ufrgs-history-plotter-server.herokuapp.com/"
        let BASE_URL = "http://localhost:5000/"
        
        
        
        // postFile(BASE_URL + "create/", content, function(response) {
        //   if (response != "erro") {
        //     getGraph(response);
        //   } else {
        //
        //     alert(response)//"Algum erro ocorreu");
        //   }
        // })
    };
    
    fr.readAsText(o.files[0]);
}

function postFile(url, file, callback) {
    var xhr = createCORSRequest('POST', url);
    
    if (!xhr) {
        throw new Error('CORS not supported');
    }
    
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        let responseText = xhr.responseText;
        
        callback(responseText);
    }
    
    var data = {
        file : file
    }
    
    dataAsString = JSON.stringify(data)
    
    xhr.send(dataAsString);
}

function getGraph(url) {
    var _img = document.getElementById('resulting_image');
    var newImg = new Image;
    
    newImg.onload = function() {
        _img.src = this.src;
    }
    newImg.src = url;
}

