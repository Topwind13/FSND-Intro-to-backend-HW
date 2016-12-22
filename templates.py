import os
import webapp2
import jinja2
import string

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
        self.render("Rot13.html", text = 'test')

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

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rot13',Rot13Page)
                               ],
                              debug = True)
