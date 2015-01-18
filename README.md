SmartNinja web app
==========

1. Install Git Flow: http://danielkummer.github.io/git-flow-cheatsheet/
2. Clone the project
3. Do ```git flow init``` to set up git flow
4. Do NOT do any development on the master branch
5. Use git flow features to develop new things (see the Git Flow Cheatsheet above)
6. Create secret.py file in app/utils and include MailChimp data ([example here](https://github.com/mailchimp/mcapi2-python-examples/blob/master/django/mcapi_python_example/utils.py))
7. Use ```appcfg.py --oauth2 update /path/to/folder/``` or ```appcfg.py --oauth2 update ./``` for pushing to GAE