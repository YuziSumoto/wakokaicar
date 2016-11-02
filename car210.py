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
from DatOil  import *   # 車検データ

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
                       ,'SnapOil':DatOil().GetSnap(int(SortNo)) # 一覧内容
                        }
    path = os.path.join(os.path.dirname(__file__), 'car210.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Rec = {}

    SortNo = int(self.request.cookies.get('SortNo', '')) # 無ければ異常終了させる

    if self.request.get('BtnEnd')  != '': # 更新ボタン
      Rec = DatOil()
      Rec.SortNo  = SortNo
      Rec.Hizuke  = datetime.datetime.strptime(self.request.get('Hizuke'), '%Y/%m/%d')
      Rec.Kyori   = int(self.request.get('Kyori'))
      Rec.Element = int(self.request.get('Element'))
      Rec.Biko    = self.request.get('Biko')
      DatOil().AddRec(Rec)

    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 明細選択
        Rec = DatOil().GetRec(SortNo,datetime.datetime.strptime(self.request.get('BtnSel'), '%Y/%m/%d')) 
      if "BtnDel" in param:  # 明細削除
        DatOil().Delete(SortNo,datetime.datetime.strptime(param.replace("BtnDel",""), '%Y/%m/%d'))
        Rec = {} 

    template_values = { 'LblMsg': ""
                       ,'Rec'       :Rec
                       ,'SnapOil':DatOil().GetSnap(int(SortNo)) # 一覧内容
                        }
    path = os.path.join(os.path.dirname(__file__), 'car210.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/car210/', MainHandler)
], debug=True)
