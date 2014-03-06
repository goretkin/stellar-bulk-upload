import os

l = os.listdir('.')

"""
https://stellar.mit.edu/S/course/6/sp14/6.036/assignments/change/editgrade.html?assgnmnt=assignments/assignment1&student=viettran@mit.edu
"""

def username_from_filename(fn):
    return fn[:-6]

def list_pdfs():
    r = []
    for n in os.listdir('.'):
        if not n[-4:] == '.pdf':
            continue
        r.append(n)
    return r

def all_pdf_names():
    r = []
    for n in list_pdfs():
        r.append(username_from_filename(n))
    return r


def upload_all_grades():
    f = open('grades.txt')

    for l in f:
        u = l.split(' ')[0]
        g = l.split(' ')[1]
        g.strip()
        if len(g)==0:
            raise AssertionError('user: %s has no grade',u)
        g = int(g)
        print u,g
        upload(u,g)

def upload_all_pdfs():
    fs = list_pdfs()
    for fn in fs:
        user = username_from_filename(fn)
        print fn, user
        f = open(fn)

        comment = "Please find a corrected PDF attached. Sorry about the delay."
        upload_comment(user,comment,f)
        f.close()


import mechanize
import cookielib
import getpass


# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(False)
br.set_debug_redirects(True)
br.set_debug_responses(False)

# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def auth():
    r = br.open('https://stellar.mit.edu/S/course/6/sp14/6.036/assignments/assignment1/')

    if br.title() == 'Account Provider Selection':
        br.select_form(nr=1)
        r = br.submit() #auth with Touchstone

    if not br.title() == 'Touchstone@MIT : Please Authenticate':
        view(r.read())
        raise AssertionError

    br.select_form(nr=1) #auth with kerberos username
    br.form['j_username'] = raw_input('Kerberos Username: ')
    br.form['j_password'] = getpass.getpass()
    r = br.submit()
    #since your browswer does not support javascript, hit submit once
    br.select_form(nr=0)
    r = br.submit()


def view(s):
    """
    view(br.open(url).read()) saves page HTML into file
    """
    f = open('blah.html','w')
    f.write(s)
    f.close()


def upload_comment(uname,comment,file=None):
    s = 'https://stellar.mit.edu/S/course/6/sp14/6.036/assignments/change/addcomment.html?assgnmnt=assignments/assignment1&student='
    ss = s + uname

    backurl = 'https://stellar.mit.edu/S/course/6/sp14/6.036/homework/assignment1/'
    backurl += uname + '/' 

    entry = br.open(ss)

    if not br.title()=='Add Comment':
        raise ValueError("At wrong page. Student/Assignment doesn't exist or not authenticated. Title: %s"%(br.title()))
        
    br.select_form(nr=0)

    assert br.form['privateComment'][0]=='true'

    #Stellar does annoying javascript stuff that we have to replicate here so that the server accepts the request
    br.form['newCommentRaw'] = comment
    br.find_control('newComment').readonly = False 
    br.form['newComment'] = comment

    br.find_control('backURL').readonly = False
    br.form['backURL'] = backurl

    if file is not None:
        br.form.add_file(file,content_type='application/pdf',filename="%s_corrected.pdf"%(uname))
    br.submit()

def upload(uname,grade):
    s = 'https://stellar.mit.edu/S/course/6/sp14/6.036/assignments/change/editgrade.html?assgnmnt=assignments/assignment1&student='
    ss = s + uname

    gradeentry = br.open(ss)
    if not br.title() == 'Edit Grade':
        raise ValueError("At wrong page. Student/Assignment doesn't exist or not authenticated. Title: %s"%(br.title()))
    br.select_form(nr=0)

    br.form['newGrade'] = str(float(grade)) #make sure grade is a numeric string
    if len(br.form['keepGraderAnonymous']) == 0 or (not br.form['keepGraderAnonymous'][0] == 'true'):
        print 'Making Anon'
    br.form.find_control('keepGraderAnonymous').items[0].selected=True
    br.submit()


