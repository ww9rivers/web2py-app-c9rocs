# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

<<<<<<< HEAD:applications/c9rocs/controllers/default.py
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
=======
# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

>>>>>>> 44362aa42948dca08ddf1b2f86ac03c69b0d48e4:applications/welcome/controllers/default.py

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.files.append(URL('static','css/smoothness/jquery-ui.css'))
    response.files.append(URL('static','js/jquery-ui.js'))
    schools = []
    for row in db(
        (db.org.address==db.address.id) \
            & (db.address.zip==db.zip.id) \
            & (db.zip.city==db.city.id)) \
            .select(db.org.id, db.org.org, db.city.city, db.city.state, db.zip.zip, orderby=db.org.org):
        schools.append({'id':row.org.id, 'org':row.org.org, 'city':row.city.city, 'st':row.city.state, 'zip':row.zip.zip})
    item = [
        ['About 9Rocs', 'about'],
        ['Source', 'source'],
        ['Installation', 'install'],
        ['Blog', 'blog'],
        ['Documentation', 'docs'],
        ['Community', 'group'],
        ['Contact', 'contact'],
        ]
    xli = []
    for xe in item:
        xli.append(LI(A(xe[0],_href=request.env.path_info+"/"+str(xe[1]))))
    leftbar = UL(xli, _class="web2py-menu-vertical",_style="display: block; visibility: visible;")
    ritebar = A(T("Register my school"), _href="/%s/account/register_org"%(request.application))
    return dict(schools=schools, left_sidebar=leftbar, right_sidebar=ritebar)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
<<<<<<< HEAD:applications/c9rocs/controllers/default.py
=======
    http://..../[app]/default/user/bulk_register
>>>>>>> 44362aa42948dca08ddf1b2f86ac03c69b0d48e4:applications/welcome/controllers/default.py
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
