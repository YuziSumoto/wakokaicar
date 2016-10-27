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
from DatCar     import *   # 所有車データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    StrTbl = self.GetTable()

    template_values = {'LblMsg': "",
                       'StrTbl': StrTbl}
    path = os.path.join(os.path.dirname(__file__), 'car000.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

#    SyokuinID = self.request.cookies.get('SyokuinID', '0')
#    if self.request.get('BtnKekka')  != '':
#      self.redirect("/stres100/?SyokuinID=" + SyokuinID)
#      return

#    for param in self.request.arguments(): 
#      if "BtnSel" in param:  # 更新ボタン？
#        Parm =  "?SyokuinID=" + SyokuinID  # Cookieより
#        Parm += "&Bango=" + param.replace("BtnSel","")  # Cookieより
#        self.redirect("/stres020/" + Parm) #
#        return

    StrTbl = "" # self.GetTable(SyokuinID)
    template_values = {'LblMsg': "",
                       'StrTbl': StrTbl}
    path = os.path.join(os.path.dirname(__file__), 'car000.html')
    self.response.out.write(template.render(path, template_values))

  def GetTable(self):

    StrTbl = ""

    Snap = DatCar().GetAll()
#    DaiBunrui = -1 # 初期化
#    TyuBunrui = -1 # 初期化

#    UserAgent = os.environ['HTTP_USER_AGENT']

    for Rec in Snap:
      
      StrTbl += "<TR><TD colspan ='2'>"  # 項目
#      StrTbl += "</TD></TR>"
#      if TyuBunrui != Rec.TyuBunrui:
#        TyuBunrui = Rec.TyuBunrui
#        if TyuBunrui >= 1:
#          StrTbl += "<TR><TD colspan ='2'>"  # 項目
#          StrTbl += u"　" + WBunrui.GetNaiyo(Rec.DaiBunrui,Rec.TyuBunrui,Rec.SyoBunrui)  # 項目
#          StrTbl += "</TD></TR>"

#      StrTbl += "<TR><TD>"  # 項目
#      StrTbl += u"　　" + Rec.Naiyo
#      StrTbl += "</TD>"

#      if UserAgent.find('iPhone') >= 0: # iPhone?
#        StrTbl += "</TR><TR>"  # 項目
#      if UserAgent.find('Android') >= 0: # Android?
#        StrTbl += "</TR><TR>"  # 項目
        
#      StrTbl += "<TD>"    # 削除ボタン
#      StrTbl += u"<input type='submit' value = '"
#      RecKotae = WKotae.GetRec(int(SyokuinID),Rec.Bango)
#      if  RecKotae == False:
#        StrTbl += u"未回答"
#      else:
#        StrTbl += RecKotae.Naiyo
#      StrTbl += "' name='BtnSel"
#      StrTbl += str(Rec.Bango)
#      StrTbl += "'  style='font-size:LARGE'>"
      StrTbl += "</TD></TR>"
    return  StrTbl 

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/car000/', MainHandler)
], debug=True)
