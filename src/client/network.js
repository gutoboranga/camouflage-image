let BASE_URL = "http://localhost:5000"

function post(bg, ov, successCompletion) {

    var data = new FormData();
    var request = new XMLHttpRequest();

    data.append('background', bg);
    data.append('overlay', ov);

    request.addEventListener('readystatechange', function(e) {
        if( this.readyState === 4 ) {

            if (request.response == 'erro') {
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
