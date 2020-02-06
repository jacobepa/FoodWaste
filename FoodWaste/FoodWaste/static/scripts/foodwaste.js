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

// addProjectLead({{ object.id }})
function addProjectLead(id) {
    window.location.href = '/qapp/project_lead/create?project_id=' + id;
}

// editProjectLead(this)
function editProjectLead(btn) {
    if ($(btn).attr('disabled')) return;
    window.location.href = '/qapp/project_lead/detail/' + $(btn).attr('id');
}

// removeProjectLead(this)
function removeProjectLead(btn) {
    if ($(btn).attr('disabled')) return;
    window.location.href = '/qapp/project_lead/delete/' + $(btn).attr('id');
}
