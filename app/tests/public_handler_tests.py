# coding=utf-8

import unittest
import webtest  # pip install webtest
import webapp2
from app.handlers.public import PublicAboutHandler


# TODO: set up google user info (currently doesn't work)
class AppTest(unittest.TestCase):
    def setUp(self):
        # Create a WSGI application.
        app = webapp2.WSGIApplication([('/', PublicAboutHandler)])
        # Wrap the app with WebTest’s TestApp.
        self.testapp = webtest.TestApp(app)

    # Test the handler.
    def testHelloWorldHandler(self):
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'text/plain')