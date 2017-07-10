# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = T("Open Chinese School")
response.subtitle = T('Open and free spirit!')
response.appname = '9Rocs'

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Wei Wang'
response.meta.description = 'Free, open source and web-based school management software, powered by web2py. Written and programmable in Python'
response.meta.keywords = 'c9rocs, web2py, python, framework'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2007-2010'


##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('Home'), False, URL('default','index'), []),
    (T('Student'), False, URL('default','index'),
     [
            (T('Classes'), False, URL('class', 'student')),
            ]
     ),
    (T('Parent'), False, URL('default','index'),
     [
            (T('Classes'), False, URL('class', 'parent')),
            (T('Students'), False, URL('parent', 'student')),
            ]
     ),
    (T('Teacher'), False, URL('default','index'),
     [
            (T('Classes'), False, URL('class', 'teacher')),
            ]
     ),
    (T('Admin'), False, URL('team', 'default', 'design/%s' % request.application),
     [
            (T('Classes'), False, URL('class', 'admin')),
            (T('Finances'), False, URL('admin', 'finance')),
            (T('Users'), False, URL('admin', 'users')),
            ]
     ),
    (T('Account'), False, None,
     [
            (T('My School'), False, URL('account', 'register_org')),
            (T('My Account'), False, URL('account', 'register_user')),
            ]
     ),
    ]
