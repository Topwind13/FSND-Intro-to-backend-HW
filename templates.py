import os
import webapp2
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **kwargs):
        t = jinja_env.get_template(template)
        return t.render(kwargs)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

class MainPage(Handler):
    def get(self):
        self.write('Hello, topp!!')

class Rot13Page(Handler):
    def get(self):
        self.render("Rot13.html")

    def rot13(self, text):
        result = ""
        for v in text:
            # Convert to number with ord.
            c = ord(v)
            # Shift number back or forward.
            if c >= ord('a') and c <= ord('z'):
                if c > ord('m'):
                    c -= 13
                else:
                    c += 13
            elif c >= ord('A') and c <= ord('Z'):
                if c > ord('M'):
                    c -= 13
                else:
                    c += 13
            # Append to result.
            result += chr(c)
        # Return transformation.
        return result

    def post(self):
        text = self.request.get('text')
        if text:
            newText = self.rot13(text)
        self.render("Rot13.html", text=newText)


class SignUpPage(Handler):
    def get(self):
        self.render("sign-up.html")

    def post(self):
        username = self.request.get('username')
        pwd = self.request.get('pwd')
        verify_pwd = self.request.get('verify_pwd')
        email = self.request.get('email')
        have_errors = False
        params = dict(username = username,
                      email = email)
        if not valid_username(username):
            params['error_username'] = "That's not a valid username"
            have_errors = True

        if not valid_pwd(pwd):
            params['error_pwd'] = "That's not a valid password"
            have_errors = True
        elif pwd != verify_pwd:
            params['error_verify_pwd'] = "Your passwords doesn't match"
            have_errors = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email"
            have_errors = True

        if have_errors:
            self.render('sign-up.html', **params)
        else:
            self.redirect('/welcome?username='+username)

class WelcomePage(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/sign-up')


def valid_username(username):
    RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return RE.match(username)

def valid_pwd(pwd):
    RE = re.compile(r"^.{3,20}$")
    return RE.match(pwd)

def valid_email(email):
    RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return RE.match(email)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rot13', Rot13Page),
                               ('/sign-up', SignUpPage),
                               ('/welcome', WelcomePage)
                               ],
                              debug = True)
