import gettext
from c9r import jslib, jquery
t = gettext.gettext


@auth.requires_login()
def admin():
    response.view = 'classes.html'
    jslib.use_ui()
    jslib.use_grid()
    jslib.use_app('js/course.js')
    grid = jquery.Grid("class", {
            'grid': {
                'data': {
                    'url':	URL("classinfo.json"),
                    'editurl':	URL("classinfo_edit"),
                    'colNames': [ t("ID"), t("Class"), t("Teacher"), t("Schedule"), t("Summary"),
                                  t("Room"), t("Capacity"), t("Enrollment")],
                    'colModel': [
                        {'name': "id", 'index': "id", 'width': 60, 'editable': False },
                        {'name': "name", 'index': "name", 'width': 100,
                         'editable': True, 'editoptions': {'size': 10} },
                        {'name': "teacher", 'index': "teacher", 'width': 160, 'sortable': True,
                         'editable': True },
                        {'name': "sched", 'index': "sched", 'width': 200, 'sortable': True,
                         'editable': True, 'editoptions': {'size': 10} },
                        {'name': "summary", 'index': "summary", 'width': 400, 'align': "center",
                         'editable': True, 'edittype': "textarea", 'editoptions': { 'rows': 4, 'cols': 80 }},
                        {'name': "room", 'index': "room", 'width': 80, 'align': "center",
                         'editable': True, 'editoptions': {'size': 10} },
                        {'name': "capacity", 'index': "capacity", 'width': 100, 'align': "center",
                         'editable': False, 'sortable': True },
                        {'name': "enroll", 'index': "enroll", 'width': 100, 'align': "center",
                         'editable': False, 'sortable': True },
                        ],
                    'sortname': "name",
                    'sortorder': "asc",
                    'viewrecords': True,
                    'caption': t("Class Information"),
                    },
                },
            'pager': {
                'data': { 'edit': True, 'add': True, 'del': True, 'search': False, 'view': True },
                'add': { 'width': '60em', 'height': "100%", 'closeOnEscape': True, 'closeAfterAdd': True, 'closeAfterEdit': True, },
                'edit': { 'width': '60em', 'height': "400", 'closeOnEscape': True },
                'view': { 'width': '40em', 'height': "100%", 'closeOnEscape': True },
                }
            })
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("Ann-Hua Classes"),
                main_content=DIV(jquery.Help(), grid),
                rsidebar=T('Browse'),
                pagedata=jslib.Session(),
               )

@auth.requires_login()
def classinfo():
    """
    Handler of the class grid data URL.
    Returns a list of class information records that match a given set of search criteria.
    """
    response.view = 'generic.json'
    tr = []
    classinfo = db((db.classinfo.teacher==db.auth_user.id)\
                   & (db.classloc.course==db.classinfo.id)\
                   & (db.classloc.room==db.classroom.id))
    for row in classinfo.select(db.classinfo.ALL, db.classroom.ALL,
                                db.auth_user.first_name, db.auth_user.last_name):
        id = row.classinfo.id
        tr.append(dict(id = id, cell = [id, row.classinfo.course,
                                        "%s %s" % (row.auth_user.first_name, row.auth_user.last_name),
                                        row.classinfo.schedule, row.classinfo.intro,
                                        "%s-%s" % (row.classroom.building, row.classroom.room),
                                        row.classinfo.max, row.classinfo.count]))
    return dict(page=1, total=1, records=len(tr), rows=tr)

@auth.requires_login()
def classinfo_add():
    '''
    Add class information in database using posted data.

    request.post_var
 
    id          "_empty" if "add", otherwise, the record id.
    name        Name of the class.
    teacher     Name of the teacher.
    sched       Scheduled time.
    summary     Brief introduction of the class.
    room        Room name (label).
    enroll      Current number of students enrolled in this class.
    '''
    post = request.post_vars
    teacher = db(db.auth_user.username == post.teacher).select()
    db.classinfo.insert(
        course = post.name,
        teacher = teacher.id,
        schedule = post.sched,
        count = post.enroll,
        intro = post.summary)

@auth.requires_login()
def classinfo_del():
    '''
    Delete class information in database using posted data.
    '''
    pass

@auth.requires_login()
def classinfo_edit():
    '''
    Take data posted from the admin() grid to add/delete/edit class information.

    Posted variables (request.post_var):
 
    id          "_empty" if "add", otherwise, the record id.
    name        Name of the class.
    teacher     Name of the teacher.
    sched       Scheduled time.
    summary     Brief introduction of the class.
    room        Room name (label).
    enroll      Current number of students enrolled in this class.
    oper        add/edit/del
    '''
    response.view = 'generic.json'
    # Process posted data based on operator
    return {
        'add': classinfo_add,
        'del': classinfo_del,
        'edit': classinfo_update
        } [request.post_vars.oper]()

@auth.requires_login()
def classinfo_update():
    '''
    Update class information in database using posted data.
    '''
    pass

@auth.requires_login()
def parent():
    response.view = 'classes.html'
    content = T("")
    title = T("My Students' Classes") if auth.has_membership('parent') else T("Not yet")
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=title,
                main_content=content,
                rsidebar=T('Browse'),
                pagedata=jslib.Session(),
                )

@auth.requires_membership('student')
def student():
    response.view = 'classes.html'
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("My Classes"),
                main_content=T(""),
                rsidebar=T('Browse'),
                pagedata=jslib.Session(),
                )

@auth.requires_membership('teacher')
def teacher():
    response.view = 'classes.html'
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("Classes I Teach"),
                main_content=T(""),
                rsidebar=T('Browse'),
                pagedata=jslib.Session(),
                )

if __name__ == '__main__':
    import doctest
    doctest.testmod()
