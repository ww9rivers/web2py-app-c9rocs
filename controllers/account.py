@auth.requires_login()
def register_org():
    form = SQLFORM(db.org)
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def register_user():
    '''
    This controller function needs to be re-designed to display a user account,
    with all information pertinent to the user's roles: admin, student, parent,
    teacher, etc.
    '''
    response.view = 'generic.html'
    form1 = SQLFORM(db.address)
    form2 = SQLFORM(db.city)
    if form1.accepts(request.vars, session) or form2.accepts(request.vars, session):
        response.flash = 'form accepted'
    elif form1.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=DIV(form1, form2))
