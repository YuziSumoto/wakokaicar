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
from MstSyaryo  import *   # 車両マスタ
from MstSyozai  import *   # 所在マスタ
from MstSyasyu  import *   # 車種マスタ
from DatCar     import *   # 所有車データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return
    SortNo = self.request.get('SortNo')
    if SortNo == "":
      Rec = {}
    else:
      Rec = DatCar().GetRec(SortNo)
      setattr(Rec,"Keika",self.GetKeika(Rec.Nensiki))

    template_values = { 'LblMsg': ""
                       ,'Rec': Rec
                       ,'SnapSyozai': MstSyozai().GetAll() # コンボボックス用
                       ,'SnapSyasyu': MstSyasyu().GetAll() # コンボボックス用
                      }
    path = os.path.join(os.path.dirname(__file__), 'car100.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return
    self.AddRec() # レコード更新
    self.redirect("/")
    return
  
    Rec = {}
    # 更新モードなら現データセット

    template_values = { 'LblMsg': ""
                       ,'Rec': Rec
                       ,'SnapSyozai': MstSyozai().GetAll() # コンボボックス用
                       ,'SnapSyasyu': MstSyasyu().GetAll() # コンボボックス用
                      }
    path = os.path.join(os.path.dirname(__file__), 'car100.html')
    self.response.out.write(template.render(path, template_values))

  def AddRec(self):
    DatCar().Delete(self.request.get('SortNo'))
    NewRec = DatCar()
    NewRec.SortNo   = int(self.request.get('SortNo'))
    NewRec.CarNo    = self.request.get('CarNo')

    NewRec.SyozaiCD = int(self.request.get('SyozaiCD'))
    NewRec.Syozai   = MstSyozai().GetRec(self.request.get('SyozaiCD')).Name
    
    NewRec.SyasyuCD = int(self.request.get('SyasyuCD'))
    RecSyasyu = MstSyasyu().GetRec(NewRec.SyasyuCD)
    NewRec.Syasyu   = RecSyasyu.Name

    NewRec.MakerCD  = RecSyasyu.MakerCD
    NewRec.Maker    = MstMaker().GetRec(NewRec.MakerCD).Name

    NewRec.SyaryoCD = RecSyasyu.SyaryoCD
    NewRec.Syaryo   = MstSyaryo().GetRec(NewRec.SyaryoCD).Name

    NewRec.Nensiki  = datetime.datetime.strptime(self.request.get('Nensiki'), '%Y/%m/%d')
    NewRec.Biko     = self.request.get('Biko')
    NewRec.YukoFlg  = True
    NewRec.put()
    return

  def GetKeika(self,Nensiki):
    if str(Nensiki) == "":
      return ""
    Nensu  = datetime.datetime.now().year  - Nensiki.year
    Tukisu = datetime.datetime.now().month  - Nensiki.month
    if Tukisu < 0:
      Nensu  -=1
      Tukisu +=12

    return str(Nensu) + "." + str(Tukisu)
  
app = webapp2.WSGIApplication([
    ('/car100/', MainHandler)
], debug=True)
