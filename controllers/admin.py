import gettext
from c9r import jslib, jquery
t = gettext.gettext

def finance():
    pass

@auth.requires_login()
def users():
    """
    /c9rocs/admin/users
    """
    response.view = 'classes.html'
    jslib.use_ui()
    jslib.use_grid()
    jslib.use(['js/course.js'], request.application)
    grid = jquery.Grid("class", {
            'grid': {
                'data': {
                    'url':	URL("userlist.json"),
                    'editurl':	URL("userinfo_edit"),
                    'colNames': [ t("ID"), t("Name"), t("Phone"), t("Email"), t("Address"), t("Role")],
                    'colModel': [
                        {'name': "id", 'index': "id", 'width': 60, 'editable': False },
                        {'name': "name", 'index': "name", 'width': 100, 'editable': True },
                        {'name': "phone", 'index': "phone", 'width': 160, 'sortable': True, 'editable': True },
                        {'name': "email", 'index': "email", 'width': 200, 'sortable': True, 'editable': True,
                         'editoptions': {'size': 80} },
                        {'name': "address", 'index': "address", 'width': 400, 'align': "center",
                         'editable': True, 'edittype': "textarea", 'editoptions': { 'rows': 4, 'cols': 80 }},
                        {'name': "role", 'index': "role", 'width': 80, 'align': "center", 'editable': True,
                         'editoptions': {'size': 60} },
                        ],
                    'sortname': "name",
                    'sortorder': "asc",
                    'viewrecords': True,
                    'caption': t("User Information"),
                    },
                },
            'pager': {
                'data': { 'edit': True, 'add': True, 'del': True, 'search': True, 'view': True },
                # View options
                #'add': { 'width': '60em', 'height': "100%", 'closeOnEscape': True },
                'add': { 'closeOnEscape': True, 'closeAfterAdd': True, 'closeAfterEdit': True, },
                #'edit': { 'width': '60em', 'height': "400", 'closeOnEscape': True },
                #'view': { 'width': '40em', 'height': "100%", 'closeOnEscape': True },
                }
            })
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("Ann-Hua Users"),
                main_content=grid,
                rsidebar=T('Browse'),
                pagedata=jslib.Session(),
               )

def userlist():
    response.view = 'generic.json'
    return dict(page=1, total=1, records=2,
                rows=[dict(id=1, cell=[1, "Wei Wang", "734-418-8385", "ww@9rivers.com", "1032 First Street, Ann Arbor, MI 48103", "parent"]),
                      dict(id=2, cell=[2, "Lin Li", "734-418-8256", "linabc@gmail.com", "1032 First Street, Ann Arbor, MI 48103", "parent"]),
                      ])

def userinfo_edit():
    '''
    Add/delete/edit user information.

    id          User information record id.
    name        User name.
    phone       User phone number.
    email       User email address.
    address     User home address.
    role        User role(s): Admin, Parent, Student, Teacher, 
    '''
    pass
