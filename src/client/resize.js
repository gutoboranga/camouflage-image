
function getKonvaOverlay() {

    let konva = document.getElementsByClassName('konvajs-content')[0];
    let canvas = konva.children[0]

    removeAnchors();

    return canvas.toDataURL();
}

function getBackgroundSize() {
    var img = new Image()
    img.src = background

    return [img.width, img.height]
}

function resizeOverlay(width, height, ov, completion) {
    let canvas = document.createElement('canvas');

    canvas.width = width;
    canvas.height = height;

    var context = canvas.getContext("2d");

    // context.drawImage(overlay, 0, 0, width, height);

    var img = new Image();
    img.src = ov;

    img.onload = function() {
        context.drawImage(img, 0, 0, width, height);

        var dataurl = canvas.toDataURL("image/png");
        completion(dataurl);
    }
}
