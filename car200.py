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
from DatSyaken  import *   # 車検データ

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
                       ,'SnapSyaken':DatSyaken().GetSnap(int(SortNo)) # 一覧内容
                        }
    path = os.path.join(os.path.dirname(__file__), 'car200.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Rec = {}

    SortNo = int(self.request.cookies.get('SortNo', '')) # 無ければ異常終了させる

    if self.request.get('BtnEnd')  != '': # 更新ボタン
      Rec = DatSyaken()
      Rec.SortNo  = SortNo
      Rec.Hizuke  = datetime.datetime.strptime(self.request.get('Hizuke'), '%Y/%m/%d')
      Rec.Kankaku = int(self.request.get('Kankaku'))
      Rec.Biko    = self.request.get('Biko')
      DatSyaken().AddRec(Rec)

    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        Rec = DatSyaken().GetRec(SortNo,datetime.datetime.strptime(self.request.get('BtnSel'), '%Y/%m/%d')) 
      if "BtnDel" in param:  # 明細削除
        DatSyaken().Delete(SortNo,datetime.datetime.strptime(param.replace("BtnDel",""), '%Y/%m/%d'))
        Rec = {} 

    template_values = { 'LblMsg': ""
                       ,'Rec'       :Rec
                       ,'SnapSyaken':DatSyaken().GetSnap(int(SortNo)) # 一覧内容
                        }
    path = os.path.join(os.path.dirname(__file__), 'car200.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/car200/', MainHandler)
], debug=True)
