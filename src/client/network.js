let BASE_URL = "http://localhost:5000"

function postFiles(bg, ov, successCompletion, completion) {

    var data = new FormData();
    var request = new XMLHttpRequest();

    data.append('background', bg);
    data.append('overlay', ov);

    request.addEventListener('readystatechange', function(e) {
        if( this.readyState === 4 ) {

            completion();

            if (request.response == 'erro' || request.response == null || request.response == '') {
                alert('Algum erro aconteceu :(')
            } else {
                successCompletion(request.response);
            }
        }
    });

    request.responseType = 'text';

    let url = BASE_URL + "/create"

    request.open('post', url);
    request.send(data);
}
