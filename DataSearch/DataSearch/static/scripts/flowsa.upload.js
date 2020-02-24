// https://simpleisbetterthancomplex.com/tutorial/2016/11/22/django-multiple-file-upload-using-ajax.html
function loadedScripts() {
    sessionStorage.setItem('file-upload-loaded', true);
    setTimeout(function () {
        sessionStorage.removeItem('file-upload-loaded', undefined)
    }, 200);
}

$(function () {
    if (!sessionStorage.getItem('file-upload-loaded')) {
        loadedScripts();
        /* 1. OPEN THE FILE EXPLORER WINDOW */
        $(".js-upload-files").click(function () {
            $("#fileupload").click();
        });

        /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
        $("#fileupload").fileupload({
            dataType: 'json',
            done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
                if (data.result.is_valid) {
                    $("#gallery tbody").prepend(
                        "<tr><td><a href='" + data.result.download_url + "'>" + data.result.name + "</a></td>" +
                        "<td><a href='" + data.result.delete_url +
                        "' onclick='return confirm(\"Are you sure? This will delete the file from the server.\")'>" +
                        "Delete File</a></td></tr>"
                    )
                }
            }
        });
    }
});
