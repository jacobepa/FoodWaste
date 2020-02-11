// NOTE: This is critical! Bootstrap Flatly attaches fade to the popover element, so it must be removed manually.
//       If not removed, the fade class renders popover elements invisible.
function delayRemoveFade() {
    setTimeout($('.fade').removeClass('fade'), 300);
}

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

//////////////////////////////////////////////////////////////////////
// Project Lead Section
function addProjectLead(id) {
    window.location.href = '/qar5/project_lead/create?qapp_id=' + id;
}

function editProjectLead(btn) {
    if ($(btn).attr('disabled')) return;
    window.location.href = '/qar5/project_lead/detail/' + $(btn).attr('id');
}

function removeProjectLead(btn) {
    if ($(btn).attr('disabled')) return;
    window.location.href = '/qar5/project_lead/delete/' + $(btn).attr('id');
}

//////////////////////////////////////////////////////////////////////
// Project Approval Signature Section
function addApprovalSignature(id) {
    window.location.href = '/qar5/approval_signature/create?qapp_id=' + id;
}

function editApprovalSignature(btn) {
    if ($(btn).attr('disabled')) return;
    window.location.href = '/qar5/approval_signature/detail/' + $(btn).attr('id');
}

function removeApprovalSignature(btn) {
    if ($(btn).attr('disabled')) return;
    window.location.href = '/qar5/approval_signature/delete/' + $(btn).attr('id');
}

//////////////////////////////////////////////////////////////////////