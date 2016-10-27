#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template

import datetime

# ログイン認証用
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
#from MstUser   import *   # 使用者マスタ
from MstMaker  import *   # メーカマスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Snap = MstMaker().GetAll()
    template_values = { 'LblMsg': ""}
    path = os.path.join(os.path.dirname(__file__), 'car920.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Code = self.request.get('Code')
    Name = self.request.get('Name')

    MstMaker().Add(Code,Name)

    Snap = MstMaker().GetAll
    template_values = { 'LblMsg': ""}
    path = os.path.join(os.path.dirname(__file__), 'car920.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/car920/', MainHandler)
], debug=True)
