# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# perms.py
# A collection of functions to determine the permissions of pages in QA Track.
#
# Permission levels:
#   Admin - Has no restrictions and can access entire site, edit all records, and access the Django admin tool.
#   Editor - Can edit and create records within their lab but cannot outside of their lab. Can manage users but not create Admins.
#   Reader - Cannot edit or create any records.
#
# Applying permissions to a tab is a 3 step process:
#   1. Apply the @apply_perms decorator to all the def's in views.py (easy)
#   2. Apply the kwargs={'perms':'deny'} to all the non-public urls in urls.py (easy)
#   3. Set up perms.py to know what model to look at when deciding whether an editor has the same
#      lab as a record. (harder)
#
#
# # # # # # #
#
# How apply permissions to a view:
#
#   # views.py
#   from constants.perms import apply_perms
#
#   @apply_perms
#   def my_view(request,**kwargs): # **kwargs must always be set!
#       ...
#
#   class my_view_class:
#       @apply_perms
#       def get(request,**kwargs):
#           ...
#
# # # # # # #
#
# How to set up perms in urls.py
#
# Public and private urls are separated into sections, but this is NOT what determines a public or private url.
# To restrict a url you just add kwargs={'perms':'deny'} before the "name" keyword.
#   #
#   #Public URLS
#   #
#   url(r'^$', index),
#   url(r'^index/$', index, name='go_to_audits_tab'),
#   url(r'^search/$', search_audits_tab, name='search_audits_tab'),
#
#
#   #
#   # Editor/Admin URLs (Add kwargs after view and before name)
#   #
#   url(r'^create/$', AuditsTabCreateView.as_view(), kwargs={'perms':'deny'}, name='create_audits_tab_item'),
#   url(r'^create/(?P<obj_id>\d+)/$', AuditsTabCreateView.as_view(), kwargs={'perms':'deny'}, name='create_audits_tab_item'),
#
#
# # # # # # #
# How to set up perms.py to apply to a new view:
#
# The variable qualname_model_ref maps a specific tab to the objects it deals with. For example:
#
#   from audits_tab.models import *             # Make sure you import the models.
#
#   qualname_model_ref = {
#       "audits_tab": {                         # For the tab audits_tab, set by the url.
#           "default":AuditsTab,                # This is the default, or "parent" model
#           "show_deficiency":Deficiency,       # for the view show_deficiency, the model is Deficiency
#           "a_view_class.get":AuditAttachment, # If a view is a class, the qualname is <the_class>.<the_method>
#           "a_complex_view":GetComplexAssoc    # You can also define a method which takes a record_id and returns a lab_id or list of lab_ids
#           ...}
#   ...}
#
#
#   parent_model_fields = {                     # The way "parent models" are defined is not consistent across the site
#       'audits_tab':'auditstab_id',            # So if a sub-model has a foreign key to an audit, it's field in the database is auditstab_id
#       ...}
#
#
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import inspect
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.conf import settings

#Models
from django.contrib.auth.models import User
from projects.models import *
from support.models import *
from organization.models import *
import rms.models as rms

#To quickly debug perms, toggle verbose = True
verbose = False
def _print(*msg):
    if verbose:
        print(*msg)
#
#Custom functions to find more complex relationships between objects
#

#A notebook review attachment is editable if the editor lab is the same as the reviewed notebook's lab
def getNBAttachmentLab(rec_ids):
    att = NotebooksTabReviewAttachment.objects.filter(pk__in=rec_ids)
    return att[0].review.nbtab.lab_id if att.count() > 0 else 0

#A user notebook's record is editable if the editor has the same lab as the user.
def getNBUserLab(rec_ids):
    user = User.objects.filter(pk__in=rec_ids)
    return user[0].userprofile.lab_id if user.count() > 0 else 0

def getNBUserAndNBLabs(rec_ids):
    _print("RECIDS", rec_ids)
    user = User.objects.filter(pk=rec_ids[1])
    user_lab = user[0].userprofile.lab_id if user.count() > 0 else 0
    nb = NotebooksTab.objects.filter(pk=rec_ids[0])
    nb_lab = nb[0].lab_id if nb.count() > 0 else 0
    return [ user_lab, nb_lab ]

# Used for creating a notebook review.
# Given a user and/or notebook id, this returns the lab ids of all the notebooks associated with the user,
# and all the users associated with the notebook. Only a user OR notebook id should be passed, but it can handle both.
def getUserNBLabs(rec_ids):
    lab_ids = []

    if rec_ids[0] != 0: #we have a nb id
        nb = NotebooksTab.objects.filter(pk=rec_ids[0]).first()
        lab_ids.append(nb.lab_id)
        user_nbs = NotebooksTab_User_Notebooks.objects.filter(nbtab_ids__contains=[nb.id])
        for user_nb in user_nbs:
            lab_ids.append(user_nb.user.userprofile.lab_id)

    if rec_ids[1] != 0: #we have a user id
        user = User.objects.filter(pk=rec_ids[1]).first()
        lab_ids.append(user.userprofile.lab_id)
        user_nbs = NotebooksTab_User_Notebooks.objects.filter(user=user).first()
        for nb_id in user_nbs.nbtab_ids:
            nb = NotebooksTab.objects.filter(pk=nb_id).first()
            if nb is not None:
                lab_ids.append(nb.lab_id)

    _print(lab_ids)

    return list(set(lab_ids))

#A QA Actvity should be editable by its labs users but also its project's labs users
def getQlogLabs(rec_ids):
    qlog = ProjectLog.objects.filter(pk__in=rec_ids)
    lab_id = qlog[0].lab_id if qlog.count() > 0 else 0
    proj_lab_id = qlog[0].project.lab_id if qlog.count() > 0 else 0
    return [ lab_id, proj_lab_id ]

#
# Editors can attach/edit all RMS projects so return all labs.
#
def getRMS(rec_ids):
    all_labs = Lab.objects.all()
    return [ lab.id for lab in all_labs ]



#
# To see if editors have permissions to change a record, we need to
# know what urls obj_id's are referring to what model.
#
qualname_model_ref = {
        "index":{"default":None},
        "about":{"default":None},
        "accounts":{
            "default":User
            },
        "metrics" : {
            "default":Project
            },
        "organization":{
            "default":Lab
            },
        "projects" : {
            "default":Project,
            "delete_proj_org":Project_Orgs,
            "delete_project_attachment":ProjectAttachment,
            "switch_qapp_review_file_flag":ProjectAttachment,
            "switch_latest_qapp_flag":ProjectAttachment,
	        "delete_project_attachment_log":ProjectAttachment,
            },
        "qlog" : {
            "default":getQlogLabs,
            "create_project_log_no_tlp":Project,
            "file_upload_qa_review":getQlogLabs,
            },
        "qlog_review" : {
            "default":getQlogLabs,
            },
        "reports" : {
            "default":Project
            },
        "rms" : {
            "default":getRMS
            },
        "support" : {
            "default":Support
            }
        }

parent_model_fields = {
        "index":"",
        "about":"",
        "accounts":"user_id",
        'metrics':'',
        "organization":'lab_id',
        'projects':'project_id',
        'qlog':'project_log_id',
        'reports':'',
        'rms':'project_id',
        'support':'support_id',
        }

#
# Page to render if user is denyed their requested page.
#
def denyPage(request,**kwargs):
    email = settings.SUPPORT_EMAIL
    return render(request, 'main/deny_view.html', locals())


#
# Returns the argument in the arg tuple which is a WSGIRequest instance
#
def get_request(arg_tup):
    request = None
    for arg in arg_tup:
        if isinstance(arg,WSGIRequest):
            request = arg
    return request


#Projects and qa activities are "different tabs", but don't follow the same url rules as the other tabs.
def get_tab(splpath):
    if len(splpath) == 0:
        return "index"

    if splpath[0] == 'projects':
        #PROJECT LAB IS NOT THE SAME AS QLOG LAB. USERS FROM BOTH LABS HAVE TO EDIT QLOGS
        try:
            if splpath[1] == 'qlog':
                return 'qlog'
            elif splpath[1] == 'qa_review' or splpath[1] == 'qlog_qa_review':
                return 'qlog'
            else:
                return 'projects'
        except:
            return 'projects'
    else:
        return splpath[0]


#
# Pulls record info out of a URL path.
# Example:
#    record_info_from_path("sop_tab/sop_attachment/update_latest_sop_flag/1722/",sop_url_model_ref)
#       >>> (sop_tab, SOPTabAttachment, SOPTab, update_latest_sop_flag, 1722)
#
# Logic further up the chain determines what to do with this information.
#
def record_info_from_path(path,qualname):

    splpath = path.replace('/',' ').strip().split()
    _print("SPLPATH", splpath)

    #
    #If there are records ids, they should be the end of the list. Else send empty list.
    #
    rec_ids = []
    have_rec_id = True
    i = 0
    while have_rec_id:
        i -= 1
        try:
            rec_ids.append(int(splpath[i]))
        except Exception as e:
            have_rec_id = False

    #
    # Hopefully the action is always the second to last entry in path?
    #
    try: #The action should come right before the record ids in the path.
        action_index = -1 - len(rec_ids)
        action = splpath[action_index]
    except:
        action = ""

    #
    # Hopefully the tab is the first entry
    #
    tab = get_tab(splpath)
    model_ref = qualname_model_ref[tab]
    _print("TAB",tab)


    #
    # set models
    #
    parent_model = model_ref["default"]
    model = model_ref["default"]

    if qualname in model_ref:
        model = model_ref[qualname]

    return (tab, model, parent_model, action, rec_ids)


#
# Given a request, tries to idenfity the lab of the record we are altering
#   For example, we may be altering an attachment to an SOP, so we have to idenfity
#   the lab of the SOP.
#
def get_record_lab(request,qualname):
    tab, model, parent_model, action, rec_ids = record_info_from_path(request.path,qualname)
    lab_id = 0

    #rec_id = 49540

    parent_model_field = parent_model_fields[tab]
    alt_lab_id = None

    if model is None:
        lab_id = 0

    #
    #We can pass back a function as the model which will grab the correct lab id.
    #
    elif not inspect.isclass(model):
        _print("MODEL IS NOT CLASS, MUST BE FUNCTION", model)
        lab_id = model(rec_ids)

    else:
        #If our model instance has a lab_id, grab it, else hope the parent model has a lab_id.
        if hasattr(model, parent_model_field):
            parent_model_id = getattr(model.objects.get(pk__in=rec_ids),parent_model_field)
            lab = parent_model.objects.filter(pk=parent_model_id)
            lab_id = lab[0].lab_id if lab.count() > 0 else 0
            _print("Parent has lab", lab_id)

        elif hasattr(model, "lab_id"):
            lab = model.objects.filter(pk__in=rec_ids)
            lab_id = lab[0].lab_id if lab.count() > 0 else 0
            _print("Model has lab", lab_id)

        else: # We failed to match.
            lab_id = 0
            _print("UNABLE TO IDENFITY RECORD LAB", model, parent_model, parent_model_field)

    _print("LAB ID",action, lab_id)

    return action, lab_id, alt_lab_id

#
# Logic to determine if an editor is allowed to perform an action
#
def get_editor_perm(request,perm,qualname):
    user_lab = request.user.userprofile.lab_id
    action, record_lab, alt_lab = get_record_lab(request,qualname)
    deny = False
    allow_edit = False
    _print("ACTION",action)

    # ALERT: If you make changes here, also change it in organization/query_utils.py
    # Method to allow QAMs to edit records under their old orgs.
    oldlabs = {
        'libby415': 12,
        'svandegr': 12,
        'JohnOlszewski': 12,
        'jhoelle-schwalbach': 12,
        'mbob': 12,
        'kschrantz': 12,
        'jvoit': 12,
        'dyoung11': 12,
        'RobertSWright': 12,
        'rsherm01': 14,
        'ebrady': 14,
        'citkin': 8,
        'srober03': 5,
        'ldoucet': 13,
        'bstuart': 10,
        'stong02': 10,
        'calvar02': 10,
        'mvazquez': 10,
        'jnoel02': 10,
        'mhenders': 10,
        'kgarcia': 10,
        'abaxte04': 10,
        'jpancras': 9,
        'jmarkwie': 9,
        'jlivolsi': 9,
        'jscott07': 9,
        'awatkins': 9,
        'gnelson': 9,
        'bsheedy': 9,
        'jberninger': 9,
        'dandrews': 9,
        'hferguson': 9,
        'kjarema': 9,
        'janetest': 9
    }
    if request.user.username in oldlabs:
        oldlab = oldlabs[request.user.username]
    else:
        oldlab = user_lab

    # We aren't viewing an existing record, but always allow creation
    if action == 'create' or action == 'list_for_log':
        deny = False

    # There is some record-changing functionality in search requests, never deny but maybe
    # restrict editing.
    elif action == 'search' or action == 'result' or action == 'pending_qa_review':
        deny = False
        record_lab = 0
        #It looks like if lab and lab2 are in the request (SOP Tab) lab2 is the "main org"
        if request.GET.get("lab2","") != "":
            record_lab = int(request.GET.get("lab2",0))
        elif request.GET.get("lab","") != "":
            record_lab = int(request.GET.get("lab",0))

        if record_lab == user_lab or record_lab == oldlab: #We are editing a record, the user is allowed
            _print("record lab same as user lab: allowing")
            allow_edit = True

        _print("IN SEARCH", allow_edit, record_lab, user_lab)


    else: # action == edit, update, show, delete?
        #If record lab is a list of lab ids see if user_lab is in it
        if isinstance(record_lab,list) and (user_lab in record_lab or oldlab in record_lab):
            deny = False
            allow_edit = True

        elif record_lab == user_lab or record_lab == oldlab:
            _print("record lab same as user lab: allowing", record_lab == user_lab, alt_lab == user_lab)
            deny = False
            allow_edit = True
        else:
            # if record lab != user lab, don't show edit functionality
            allow_edit = False

            # If it's a deny page, and we can't prove access, deny them.
            if perm == 'deny' or perm == 'admin':
                deny = True
            else:
                deny = False


    return (deny, allow_edit)

def apply_perms(f):
    def wrapper(*args,**kwargs):

        if "perms" in kwargs:
            _print("HAVE PERMS", kwargs["perms"])
            perm = kwargs["perms"]
        else:
            _print("NO PERMS, default to restrict below editor")
            perm = "restrict"

        if "level" in kwargs:
            _print("HAVE PERM LEVEL")
            level = kwargs["level"]
        else:
            level = "editor"

        #default behavior is to restrict edit and create and don't deny
        allow_edit = False
        allow_create = False
        deny = False

        request = get_request(args)
        user = request.user
        _print('user', request.user)

        # When logging in we don't yet have a userprofile, so skip the checks.
        if not hasattr(user,"userprofile"):
            return f(*args,**kwargs)

        #_print('user perms', user.userprofile.permissions)

        #
        # Super Users can do anything.
        #
        if user.userprofile.permissions == "ADMIN":
            allow_edit = True
            allow_create = True
            deny = False

        #
        # Editors are complicated: restricted or denied unless their lab is the same as the record or if there is no record.
        #   If a record id exists (show/edit) - Restrict or deny if record lab != user lab
        #   If no record exists (index/create) - Allow. If creating: use org select to restrict creation
        #
        if user.userprofile.permissions == "EDITOR":
            # Editors can always create
            qualname = f.__qualname__
            _print("QUALNAME",qualname)
            if perm == 'admin':
                _print("ADMIN ONLY")
                allow_create = False
                deny = True
            else:
                allow_create = True
                deny, allow_edit = get_editor_perm(request,perm,qualname)

        #
        # Readers are always restricted and always denied if perm == deny
        #
        if user.userprofile.permissions == "READER":

            # Always restrict readers.
            allow_edit = False
            allow_create = False

            # Deny reader if deny is set in URL.
            if perm == 'deny' or perm == 'admin' or perm == 'editor':
                deny = True

        #
        # If we are restricting, we pass kwargs for the templates to handle
        #
        _print("ALLOW EDIT",allow_edit)
        kwargs["allow_edit"] = allow_edit

        _print("ALLOW CREATE",allow_create)
        kwargs["allow_create"] = allow_create

        kwargs["perm_level"] = user.userprofile.permissions
        kwargs["is_admin"] = user.userprofile.permissions == "ADMIN"

        #
        # If we are denying, render the deny page.
        #
        _print("DENY",deny)
        if deny == True:
            return denyPage(request,**kwargs)

        return f(*args,**kwargs)

    return wrapper
