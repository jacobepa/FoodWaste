// NOTE: This is critical! Bootstrap Flatly attaches fade to the popover element, so it must be removed manually.
//       If not removed, the fade class renders popover elements invisible.
function delayRemoveFade() {
    setTimeout($('.fade').removeClass('fade'), 300);
}

setTimeout(function () {
    $("#save_success").addClass('fade');
}, 2000);

function fromEditToDetail() {
    var path = window.location.pathname.replace('edit', 'detail');
    window.location.href = path;
}

function rowClick(id) {
    $("tr").removeClass('table-active');
    $("#" + id).addClass('table-active');
    $("i").removeAttr('disabled');
    $("i").attr('id', id);
}
