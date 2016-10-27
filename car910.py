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
from MstSyozai  import *   # 所在マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    SnapSyozai = MstSyozai().GetAll()
    template_values = { 'LblMsg': ""}
    path = os.path.join(os.path.dirname(__file__), 'car910.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Code = self.request.get('Code')
    Name = self.request.get('Name')

    MstSyozai().Add(Code,Name)

    SnapSyozai = MstSyozai().GetAll
    template_values = { 'LblMsg': ""}
    path = os.path.join(os.path.dirname(__file__), 'car910.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/car910/', MainHandler)
], debug=True)
