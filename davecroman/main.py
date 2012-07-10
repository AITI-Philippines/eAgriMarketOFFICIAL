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
import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

homepage = """
    <title> CS 172 Prototype Page </title>
    <head><h1> Inventory Prediction System </h1> 
    <h2> Created by Aubrey's Angels </h2>
    <hr noshade>
<body>
   Welcome to our site!
   <br><br>
   <a href="/market">Target Market</a><br>
   <a href="/releases">Releases</a><br>
   <a href="/about">About</a><br>
</body>
"""

theteam = """
<title> The Team </title>
<head><h1> Inventory Prediction System </h1></head>
<hr noshade> 
<body>
<b>Francis Jomer de Leon Gallardo: </b> (insert picture here) add later, no time<<<
<br><br>
<b>Jules Capacillo</b> (insert picture here) Jules is the incumbent president of an organization based in the college of Engineering. He has experience in web development and has worked on a web application project for a local bank. His undergraduate research involves developing a tool that would help marine biologists determine fish population in their natural habitat. He is very much interested in mobile and web development
<br><br>
<b>Aubrey Joanna Pascual</b> (insert picture here) Aubrey is a student having her undergraduate thesis, under the laboratory Computer Security Group, which involves secure sharing on onion routing via peer-to-peer. She passed the PhilNITS (Philippine National IT Standards) Fundamental IT Engineer certification exam on her junior year.
<br><br>
<b>Armond Ave (insert picture here) </b> Armond is a part-time game developer who has worked for 2 games under Cartoon Network. He has had experience working with Django projects, Android apps, and Air Mobile games. His undergraduate research involves creating educational tools for children with special needs. He is very interested in the field of mobile development.
<br><br>
<b>Adviser(s): </b> Jessica May Guerrero (insert picture here)
</body>
<hr noshade><br>
<a href="/">Home</a><br>
"""

releases ="""
<head><h1> Inventory Prediction System </h1></head>
<title>Releases</title>
<hr noshade> 
<body>None</body>
<hr noshade>
<a href="/">Home</a><br>
"""

market="""
<head><h1> Inventory Prediction System </h1></head>
<title>FAQ</title>
<hr noshade> 
<h2>Customer Profile:</h2>

<ul>
<li>Gender - M/F</li>
<li>Age- 30-50</li>
<li>Region - PH</li>
<li>Occupation- Entrepreneur</li>
<li>Social Level- Medium, High</li>
<li>Characteristics- Internet Access</li>
<li>user Category Early adapters</li>
<li>Others- Willing to learn basic computer literacy</li>
</ul><h2>Total Addressable Market</h2>

<ul>
<li>Philippines -90 mil</li>
<li>Entrepreneur</li>
<li>Internet User</li>
<li>In the Retail Business</li>
</ul><h2>Persona:</h2>

<ul>
<li>Female</li>
<li>Lives in Quezon City</li>
<li>33 years old</li>
<li>Has a busy schedule (running business, family relations)</li>
<li>Owns a small supermarket</li>
<li>Fond of her IPhone</li>
<li>Loves Shopping (especially buying clothes)</li>
<li>Summer Beach person</li>
<li>70 - 90k monthly income range</li>
<li>Loves to make interesting conversations.</li>
</ul>
<hr noshade> 
<a href="/">Home</a><br>
"""

class MainHandler(webapp2.RequestHandler):
    def create_form(self, username="", email="", user_response="", password_response="", verify_response="", email_response=""):    
        return form % {"username": username, "email": email, "username_error": user_response, "password_error": password_response,
                       "verify_error": verify_response, "email_error": email_response }
        
    def get(self):
        self.response.out.write(self.create_form())
    
    def post(self):
        input_username = self.request.get('username')
        input_password = self.request.get('password')
        input_verification = self.request.get('verify')
        input_email = self.request.get('email')
        
        error_message = "Invalid"
        user_is_valid = is_user_valid(input_username)
        password_is_valid = is_password_valid(input_password)
        verify_is_valid = is_verify_valid(input_password, input_verification)
        email_is_valid = is_email_valid(input_email)
        
        user_response=""
        password_response=""
        verify_response=""
        email_response=""
        
        if not user_is_valid:
            user_response = error_message
        if not password_is_valid:
            password_response = error_message
        if not verify_is_valid:
            verify_response = error_message
        if not email_is_valid:
            email_response = error_message
     
        
        if user_is_valid and password_is_valid and verify_is_valid and email_is_valid:
            self.redirect('/welcome?username=' + input_username)
        else:
            self.response.out.write(self.create_form(input_username, input_email, user_response, password_response, verify_response, email_response))

class HomepageHandler(webapp2.RequestHandler):
    def show_homepage(self):
        return homepage
    
    def get(self):
        self.response.out.write(self.show_homepage())

class HomepageHandler(webapp2.RequestHandler):
    def show_homepage(self):
        return homepage
    
    def get(self):
        self.response.out.write(self.show_homepage())

class TeamPageHandler(webapp2.RequestHandler):
    def show_teamPage(self):
        return theteam

    def get(self):
        self.response.out.write(self.show_teamPage())
        
class ReleasesHandler(webapp2.RequestHandler):
    def show_releasesPage(self):
        return releases

    def get(self):
        self.response.out.write(self.show_releasesPage())
        
class MarketHandler(webapp2.RequestHandler):
    def show_releasesPage(self):
        return market

    def get(self):
        self.response.out.write(self.show_releasesPage())

app = webapp2.WSGIApplication([('/', HomepageHandler), ('/welcome', WelcomePageHandler), ('/about', TeamPageHandler),
                                ('/releases', ReleasesHandler), ('/market', MarketHandler),
                                ],
                              debug=True)
