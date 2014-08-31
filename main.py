#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import jinja2
import webapp2
import string
import re

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
		return USERNAME_RE.match(username)
		
def valid_password(password):
		return PASSWORD_RE.match(password)
		
def valid_email(email):
		return EMAIL_RE.match(email)



template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
		
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render('index.html')
		
class Rot13Page(Handler):
	def get(self):
		self.render('rot13.html')
		
	def post(self):
		text = self.request.get('text')
		newtext = ''
		uppers = string.ascii_uppercase
		lowers = string.ascii_lowercase
		for c in text:
			if c in lowers:
				index = lowers.find(c)
				if index > 12:
					newtext = newtext + lowers[index - 13]
				else:
					newtext = newtext + lowers[index + 13]
			elif c in uppers:
				index = uppers.find(c)
				if index > 12:
					newtext = newtext + uppers[index - 13]
				else:
					newtext = newtext + uppers[index + 13]
			else:
				newtext = newtext + c
		self.render('rot13.html', text = newtext)
		
class SignupPage(Handler):
	def renderpage(self, username, email, error_username, error_password, error_verify, error_email):
		self.render('signup.html', username=username, email=email, error_username=error_username, error_password=error_password, error_verify=error_verify, error_email=error_email)
	
	def get(self):
		self.render('signup.html')
		
	def post(self):
		error_username=""
		error_password=""
		error_verify=""
		error_email=""
	
		user_username = self.request.get('username')
		user_password = self.request.get('password')
		verify = self.request.get('verify')
		user_email = self.request.get('email')
		
		username = valid_username(user_username)
		password = valid_password(user_password)
		email = valid_email(user_email)
		
		if not (username and password and email and user_password == verify):
			if not username:
				error_username = "That's not a valid username!"
			
			if not password:
				error_password = "That's not a valid password!"
				
			if not password == verify:
				error_verify = "Passwords do not match!"
				
			if not email:
				error_email = "That's not a valid email!"
			
			self.renderpage(user_username, user_email, error_username, error_password, error_verify, error_email)
		else:
			self.redirect('/welcome?username=' + user_username)
		
		
		
		

		
		
		
class WelcomePage(Handler):
	def get(self):
		username = self.request.get('username')
		self.render('welcome.html', username=username)
		
		
class FizzBuzzPage(Handler):
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render('fizzbuzz.html', n = n)

app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/rot13', Rot13Page),
	('/signup', SignupPage),
	('/fizzbuzz', FizzBuzzPage),
	('/welcome', WelcomePage)
], debug=True)
