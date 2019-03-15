var lastInstructionShowed = 1

let instructions = [
    "Escolha uma imagem de fundo:",
    "Escolha a imagem que você deseja camuflar. O ideal é que seja uma imagem png com fundo transparente!",
    "Posicione-a sobre o fundo e quando estiver na posição correta, clique no botão abaixo:",
    "Aguarde um momento",
]

let extraHtml = [
    "<input id=\"background-input\" type=\"file\" onchange=\"didSelectBackground(this)\">",
    "<input id=\"overlay-input\" type=\"file\" onchange=\"didSelectOverlay(this)\">",
    "<input value=\"Camuflar\" type=\"submit\" onclick=\"didFinishEditing()\">",
    ""
]

var background = undefined
var overlay = undefined

// ============ Actions ============

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

        console.log("did select overlay");

        overlay = e.target.result
        updateImages();

    }

    reader.readAsDataURL(input.files[0]);

}

function didFinishEditing() {

    overlay = getKonvaOverlay()

    let size = getBackgroundSize()

    resizeOverlay(size[0], size[1], function(newOverlayData) {
        // post(background, newOverlayData);
        post(background, newOverlayData, function(resultUrl) {
            showResultingImage(resultUrl)
        });
    })

}

function showResultingImage(resultUrl) {
    canvasContainer = document.getElementById('container');
    canvasContainer.parentNode.removeChild(canvasContainer);

    document.getElementById('image').src = resultUrl;
}

// ============ Auxiliar ============

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
