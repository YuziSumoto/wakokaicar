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
from MstMaker   import *   # メーカマスタ
from MstSyaryo  import *   # 車両区分
from MstSyasyu  import *   # 車両マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    SnapSyasyu = MstSyasyu().GetAll()
    SnapMaker  = MstMaker().GetAll()
    SnapSyaryo = MstSyaryo().GetAll()
    template_values = { 'LblMsg': ""
                       ,'SnapSyasyu': SnapSyasyu
                       ,'SnapMaker' : SnapMaker
                       ,'SnapSyaryo': SnapSyaryo
                      }
    path = os.path.join(os.path.dirname(__file__), 'car940.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Code = self.request.get('Code')
    MakerCD  = self.request.get('MakerCD')
    SyaryoCD = self.request.get('SyaryoCD')
    Name     = self.request.get('Name')

    if self.request.get('BtnEnd')  != '': # 更新ボタン
      MstSyasyu().Add(Code,MakerCD,SyaryoCD,Name) # 更新
      Rec = {} 

    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        Rec = MstSyasyu().GetRec(self.request.get('BtnSel')) 
      if "BtnDel" in param:  # 明細削除
        MstSyasyu().Delete(param.replace("BtnDel",""))
        Rec = {} 

    SnapSyasyu = MstSyasyu().GetAll()
    SnapMaker  = MstMaker().GetAll()
    SnapSyaryo = MstSyaryo().GetAll()
    template_values = { 'LblMsg': ""
                       ,'Rec'       : Rec
                       ,'SnapSyasyu': SnapSyasyu
                       ,'SnapMaker' : SnapMaker
                       ,'SnapSyaryo': SnapSyaryo
                      }
    path = os.path.join(os.path.dirname(__file__), 'car940.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/car940/', MainHandler)
], debug=True)
