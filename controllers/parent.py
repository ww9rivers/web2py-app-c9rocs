import gettext
from c9r import jslib, jquery
t = gettext.gettext

@auth.requires_membership('parent')
def childlist():
    '''
    '''
    response.view = 'generic.json'
    tr = []
    childinfo = db((db.guardian.parent==auth.user.id) and (db.guardian.child==db.auth_user.id))
    for row in childinfo.select(db.auth_user.ALL):
        id = row.auth_user.id
        tr.append(dict(id = id, cell = [id,
                                        "%s %s" % (row.auth_user.first_name, row.auth_user.last_name),
                                        '',
                                        row.auth_user.email,
                                        ]))
    return dict(page=1, total=1, records=len(tr), rows=tr)

@auth.requires_login()
def student():
    """
    /c9rocs/parent/student: Page for parent(s) to manage their students.
    """
    response.view = 'classes.html'
    jslib.use_ui()
    jslib.use_grid()
    jslib.use(['js/course.js'], request.application)
    grid = jquery.Grid("class", {
            'grid': {
                'data': {
                    'url':	URL("childlist.json"),
                    'editurl':	URL("childlist_edit"),
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
                    'caption': t("Class Information"),
                    },
                },
            'pager': {
                'data': { 'edit': True, 'add': True, 'del': True, 'search': False, 'view': True },
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
