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
from DatUse  import *   # 使用データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return
    SortNo = self.request.get('SortNo')  # パラメタ取得
    cookieStr = 'SortNo=' + SortNo + ';' # パラメタ保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    template_values = { 'LblMsg': ''
                       ,'SnapUse':DatUse().GetSnap(int(SortNo)) # 一覧内容
                        }
    path = os.path.join(os.path.dirname(__file__), 'car220.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Rec = {}

    SortNo = int(self.request.cookies.get('SortNo', '')) # 無ければ異常終了させる

    if self.request.get('BtnEnd')  != '': # 更新ボタン
      Rec = DatUse()
      Rec.SortNo   = SortNo
      Rec.Hizuke   = datetime.datetime.strptime(self.request.get('Hizuke'), '%Y/%m/%d')
      Rec.STime    = datetime.datetime.strptime(self.request.get('STime'), '%H:%M')
      if  self.request.get('ETime') != "":
        Rec.ETime    = datetime.datetime.strptime(self.request.get('ETime'), '%H:%M')
      Rec.Ikisaki  = self.request.get('Ikisaki')
      Rec.Mokuteki = self.request.get('Mokuteki')
      Rec.Unten    = self.request.get('Unten')
      Rec.Douzyo   = self.request.get('Douzyo')
      if  self.request.get('Kyori') != "": 
        Rec.Kyori    = int(self.request.get('Kyori'))
      Rec.Biko     = self.request.get('Biko')
      DatUse().AddRec(Rec)

    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        Hizuke,STime =  param.replace("BtnSel","").split("-")
        Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
        STime  = datetime.datetime.strptime(STime, '%H:%M')
        Rec = DatUse().GetRec(SortNo,Hizuke,STime) 
      if "BtnDel" in param:  # 明細削除
        Hizuke,STime =  param.replace("BtnDel","").split("-")
        Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
        STime  = datetime.datetime.strptime(STime, '%H:%M')
        DatUse().Delete(SortNo,Hizuke,STime)
        Rec = {} 

    template_values = { 'LblMsg': ""
                       ,'Rec'       :Rec
                       ,'SnapUse':DatUse().GetSnap(int(SortNo)) # 一覧内容
                        }
    path = os.path.join(os.path.dirname(__file__), 'car220.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/car220/', MainHandler)
], debug=True)
