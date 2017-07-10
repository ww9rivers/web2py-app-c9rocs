# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
                                              # optional DAL('gae://namespace')
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
#    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
    db = DAL('mysql://c9rocs:v0tpvsfns@localhost/c9rocsdb')

## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:f8ce31eb-8d29-4c31-b555-6a5494aad172'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
from gluon.contrib.login_methods.rpx_account import RPXAccount
auth.settings.actions_disabled=['register','change_password','request_reset_password']
auth.settings.login_form = RPXAccount(request, api_key='e381032311a0c6b0313380b1df4e47bf8f8c4d38',domain='c9rocs',
   url = "https://%(host)s/%(app)s/default/user/login" % {'host':request.env.http_host, 'app':request.application})
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

##      Home: address, city, state zip
from gluon.contrib.states import *
db.define_table('city',
                Field('city', length=32),
                Field('state', length=2, requires=IS_IN_SET(US_STATES)),
                format='%(city)s, %(state)s')
db.define_table('zip',
                Field('zip', unique=True),
                Field('city', db.city),
                format='%(zip)s')
db.define_table('address',
                Field('strno', length=64, label=T('Street number')),
                Field('zip', db.zip, requires=IS_IN_DB(db, db.zip.id, '%(zip)s', zero=T('choose one'))))

##      Organization: Multiple origanization are supported
db.define_table('org',
                Field('org', length=32),
                Field('address', db.address, requires=IS_IN_DB(db, db.address.id, '%(strno)s, %(zip)s')),
                Field('admin', db.auth_user),
                Field('bylaw', 'text'))

##      Classinfo: data for a class at the school
db.define_table('classinfo',
                Field('course', length=32),
                Field('teacher', db.auth_user), # must be in 'teacher' auth_group
                Field('schedule', 'time'),
                Field('count', 'integer'),      # current enrollment
                Field('max', 'integer'),        # maximum enrollment
                Field('intro', length=80),
                Field('description', 'text'))

##      Classroom information: name, location, capacity, etc.
db.define_table('classroom',
                Field('room', length=16),
                Field('campus', length=16),
                Field('building', length=16),
                Field('capacity', 'integer'))

##      Classroom assignment: Relation between classinfo and classroom
db.define_table('classloc',
                Field('course', db.classinfo),
                Field('room', db.classroom))

##      Guardian: Parent/student relationship
db.define_table('guardian',
                Field('parent', db.auth_user),  # must be in 'parent' auth_group
                Field('child', db.auth_user),   # must be 'student'
                Field('address', db.address))

##      Enrollment: Class/student relationship
db.define_table('enrollment',
                Field('course', db.classinfo),
                Field('student', db.auth_user),
                Field('status', length=16))      # paid, withdrawn, ...

##      Care: Emergency (health)care information
db.define_table('care',
                Field('phsycian', length=64),
                Field('docphone', length=10),
                Field('emergency', length=64))
