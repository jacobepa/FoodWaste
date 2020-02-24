// https://simpleisbetterthancomplex.com/tutorial/2016/11/22/django-multiple-file-upload-using-ajax.html
function loadedScripts() {
    sessionStorage.setItem('flowsa-upload-loaded', true);
    setTimeout(function () {
        sessionStorage.removeItem('flowsa-upload-loaded', undefined)
    }, 1000);
}

$(function () {
    if (!sessionStorage.getItem('flowsa-upload-loaded')) {
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
                        "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
                    )
                }
            }
        });
    }
});
