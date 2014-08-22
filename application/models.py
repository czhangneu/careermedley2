
__author__ = 'onyekaigabari'


from hashlib import md5
from application import app, db, UserMixin
import flask_whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1


class User(UserMixin, db.Model):
    #__tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def avatar(self, size):
        print "show avatar"
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return 'User %r>' % (self.username)

class Account(db.Model):
    #__tablename__ = 'Account'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user_id = db.Column(db.Integer)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    zipcode = db.Column(db.Integer)
    major = db.Column(db.String(100))
    degree = db.Column(db.String(100))
    # user-account: one-to-one map
    user = db.relationship("User", backref=db.backref("account", lazy='joined', uselist=False))

    def __init__(self, user_id, firstname=None, lastname=None, city=None,
                 state = None, country=None, zipcode = 11111, major=None, degree=None):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode
        self.major = major
        self.degree = degree

    def __repr__(self):
        return 'Account %r>' % (self.firstname)


class Position(db.Model):
    __searchable__ = ['jobtitle']  # the field that will be created index
    # jobkey
    jobkey = db.Column(db.String, primary_key=True)
    # employer_name
    employername = db.Column(db.String(120))
    # title
    jobtitle = db.Column(db.String(120))
    # city
    city = db.Column(db.String(120))
    # state
    state = db.Column(db.String(80))
    # short_desc
    snippet = db.Column(db.String(300))
    # post_date
    post_date = db.Column(db.DateTime)
    # url
    url = db.Column(db.String(400))
    # expired
    expired = db.Column(db.Boolean)

    def __init__(self, jobkey, employername, jobtitle, city, state,
                 snippet, post_date, url, expired):
        self.jobkey = jobkey
        self.employername = employername
        self.jobtitle = jobtitle
        self.city = city
        self.state = state
        self.snippet = snippet
        self.post_date = post_date
        self.url = url
        self.expired = expired

    def __repr__(self):
        return '<Position %r>' % self.jobtitle


class MarkedPositions(db.Model):
    #__tablename__ = 'MarkedPositions'
    id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
    jobkey = db.Column(db.Integer, db.ForeignKey('position.jobkey'), primary_key=True)
    marked = db.Column(db.Boolean)

    account = db.relationship('Account', backref=db.backref('marked_positions', lazy='dynamic'))
    position = db.relationship('Position', backref=db.backref('marked_positions', lazy='dynamic'))


    def __init__(self, id, jobkey, marked):
        self.id = id
        self.jobkey = jobkey
        self.marked = marked

    def __repr__(self):
        return '<Position %s, Account: %d>' % self.position_id, self.account_id


class Application(db.Model):
    #__tablename__ = 'Application'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    jobkey = db.Column(db.String, db.ForeignKey('position.jobkey'), primary_key=True)
    apply_date = db.Column(db.DateTime)
    resume = db.Column(db.String(300))
    cv = db.Column(db.String(300))

    user = db.relationship('User', backref=db.backref('applications', lazy='dynamic'))
    position = db.relationship('Position', backref=db.backref('applications', lazy='dynamic'))

    def __init__(self, id, jobkey, apply_date, resume, cv):
        self.id = id
        self.jobkey = jobkey
        self.apply_date = apply_date
        self.resume = resume
        self.cv = cv

    def __repr__(self):
        return '<Application %r>' % self.accountid

#class
class Document(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    doc_name = db.Column(db.String(300), unique=True)
    doc_path = db.Column(db.String(300), unique=True)

    user = db.relationship('User', backref=db.backref('documents', lazy='dynamic'))

    def __init__(self, id, doc_name, doc_path):
        self.id = id
        self.doc_name = doc_name
        self.doc_path = doc_path

    def __repr__(self):
        return '<Account: %s, Document %s>' % (self.id, self.doc_name)

class Employer(db.Model):
    employer_name = db.Column(db.String(100), primary_key=True)
    num_ratings = db.Column(db.Integer)
    score = db.Column(db.String)
    ceo_name = db.Column(db.String(100))
    num_ceo_reviews = db.Column(db.Integer)
    # ceo_approval rate e.g. 98 -> 98%
    ceo_approval = db.Column(db.Integer)

    def __init__(self, employer_name, num_ratings, score, ceo_name,
                 num_ceo_reviews, ceo_approval):
        self.employer_name = employer_name
        self.num_ratings = num_ratings
        self.score = score
        self.ceo_name = ceo_name
        self.num_ceo_reviews = num_ceo_reviews
        self.ceo_approval = ceo_approval

    def __repr__(self):
        return '<Employer: %s>' % (self.employer_name)

# ------------------------------------------------------------------------------------
class Employer_site_login_info(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    employer_name = db.Column(db.String, db.ForeignKey('employer.employer_name'), primary_key=True)
    login_link = db.Column(db.String)
    site_id = db.Column(db.String)
    site_password = db.Column(db.String)
    site_email = db.Column(db.String)
    user = db.relationship(User, uselist=False, backref="employer_site_login_info")
    employer = db.relationship(Employer, uselist=False, backref="employer_site_login_info")

    def __init__(self, id, employer_name, login_link, site_id, site_password, site_email):
        self.id = id
        self.employer_name = employer_name
        self.login_link = login_link
        self.site_id = site_id
        self.site_password = site_password
        self.site_email = site_email

    def __repr__(self):
        return '<Employer_site_login_info | account: %s, employername: %s>' \
               % (self.id, self.employer_name)

# ------------------------------------------------------------------------------------
class Application_status(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    jobkey = db.Column(db.String, db.ForeignKey('position.jobkey'), primary_key=True)
    employer_name = db.Column(db.String, db.ForeignKey('position.employername'))
    # status: should be an enumeration type: applied | interviewing | offer or rejection
    status = db.Column(db.String)

    user = db.relationship(User, uselist=False, backref="application_status")
    position = db.relationship(Position, uselist=False, backref="application_status")

    def __int__(self, id, jobkey, employer_name, status):
        self.id = id
        self.jobkey = jobkey
        self.employer_name = employer_name
        self.status = status

    def __repr__(self):
        return '<Application_status | accountid : %s, jobkey : %s>' \
               % (self.id, self.jobkey)
# ---------------------------------------------------------------------------------------------------
# for past or future interviews
class Interview(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    jobkey = jobkey = db.Column(db.String, db.ForeignKey('position.jobkey'), primary_key=True)
    employer_name = db.Column(db.String, db.ForeignKey('position.employername'))
    interview_round = db.Column(db.Integer)
    interview_date = db.Column(db.DateTime)

    user = db.relationship(User, uselist=False, backref="application_status")
    position = db.relationship(Position, uselist=False, backref="application_status")

    def __int__(self, id, jobkey, employer_name, interview_round, interview_date):
        self.id = id
        self.jobkey = jobkey
        self.employer_name = employer_name
        self.interview_round = interview_round
        self.interview_date = interview_date

    def __repr__(self):
        return '<Interview | accountid: %s, jobkey : %s, round: %d>' \
               % (self.id, self.jobkey, self.interview_round)

# ---------------------------------------------------------------------------------------------------
class Interview_question(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    jobkey = jobkey = db.Column(db.String, db.ForeignKey('position.jobkey'), primary_key=True)
    employer_name = db.Column(db.String, db.ForeignKey('position.employername'))
    interview_round = db.Column(db.Integer)
    question = db.Column(db.String)
    solution = db.Column(db.String)
    feedback = db.Column(db.String)

    user = db.relationship(User, uselist=False, backref="application_status")
    position = db.relationship(Position, uselist=False, backref="application_status")

    def __init__(self, id, jobkey, employer_name, interview_round, queston, solution, feedback):
        self.id = id
        self.jobkey = jobkey
        self.employer_name = employer_name
        self.interview_round = interview_round
        self.question = queston
        self.solution = solution
        self.feedback = feedback

    def __repr__(self):
        return '<Interview_question | accountid: %s, jobkey : %s, round: %d, question: %s>' \
               % (self.id, self.jobkey, self.interview_round, self.question)

# ---------------------------------------------------------------------------------------------------
# create index for table: Position
whooshalchemy.whoosh_index(app, Position)