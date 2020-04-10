
function SectionBTypeChanged(e) {
    let val = $(e).val();
    console.log(val);
    // TODO Reload this page with a form for the selected section b type
    let href = window.location.href;
    if (href.includes('sectionb_type')) {
        href = href.replace(/sectionb_type=[0-9]{1,}/, 'sectionb_type=' + val);
    } else {
        href = href + '&sectionb_type=' + val;
    }
    window.location.href = href;
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
// Project Approval Section
function editApprovalPage(id) {
    window.location.href = '/qar5/approval/edit/' + id;
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