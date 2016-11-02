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
from DatSyaken  import *   # 車検データ
from DatOil     import *   # オイル交換データ
from DatUse     import *   # 使用データ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    Snap = DatCar().GetAll()
    for Rec in Snap:
      setattr(Rec,"Keika",self.GetKeika(Rec.Nensiki))
      setattr(Rec,"WNensiki",self.WarekiHenko(Rec.Nensiki))

      Zikai,FontColor = DatSyaken().GetNext(Rec.SortNo)
      setattr(Rec,"Zikai",Zikai)
      setattr(Rec,"ZikaiColor",FontColor)
      Kakunin,Kyori = DatUse().GetKyori(Rec.SortNo)
      setattr(Rec,"Kakunin",Kakunin)
      setattr(Rec,"Kyori","{:,d}".format(Kyori))

      Oil = DatOil().GetNext(Rec.SortNo)
      if Oil != 0:
        setattr(Rec,"Oil","{:,d}".format(Oil))
        if int(Kyori) > (Oil - 1000):
          setattr(Rec,"OilColor",";background-color:red")
              
    template_values = {'LblMsg': ""
                      ,'Snap': Snap 
                       }
    path = os.path.join(os.path.dirname(__file__), 'car000.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    for param in self.request.arguments(): 
      if "BtnSel" in param:  # 選択ボタン？
        self.redirect("/car100/?SortNo=" + self.request.get('BtnSel')) # パラメタ付で登録画面
        return
      if "BtnSyaken" in param:  # 車検ボタン？
        self.redirect("/car200/?SortNo=" + param.replace("BtnSyaken","")) # パラメタ付で車検画面
        return
      if "BtnOil" in param:  # オイル交換ボタン？
        self.redirect("/car210/?SortNo=" + param.replace("BtnOil","")) # パラメタ付で車検画面
        return
      if "BtnKyori" in param:  # 距離ボタン？
        self.redirect("/car220/?SortNo=" + param.replace("BtnKyori","")) # パラメタ付で車検画面
        return
      if "BtnDel" in param:  # 更新ボタン？
        DatCar().Delete(param.replace("BtnDel",""))

    Snap = DatCar().GetAll()
    for Rec in Snap:
      setattr(Rec,"Keika",self.GetKeika(Rec.Nensiki))
      setattr(Rec,"WNensiki",self.WarekiHenko(Rec.Nensiki))
      Zikai,FontColor = DatSyaken().GetNext(Rec.SortNo)
      setattr(Rec,"Zikai",Zikai)
      setattr(Rec,"ZikaiColor",FontColor)
      
      Oil = DatOil().GetNext(Rec.SortNo)
      if Oil != 0:
        setattr(Rec,"Oil","{:,d}".format(Oil))

    template_values = {'LblMsg': ""
                      ,'Snap': Snap
                      }
    path = os.path.join(os.path.dirname(__file__), 'car000.html')
    self.response.out.write(template.render(path, template_values))

  def GetKeika(self,Nensiki):
    if str(Nensiki) == "":
      return ""
    Nensu  = datetime.datetime.now().year  - Nensiki.year
    Tukisu = datetime.datetime.now().month  - Nensiki.month
    if Tukisu < 0:
      Nensu  -=1
      Tukisu +=12

    return str(Nensu) + "." + str(Tukisu)

  def WarekiHenko(self,Nensiki):
    if str(Nensiki) == "":
      return ""
    Nen  = Nensiki.year  - 1988
    Wareki =  "H" + str(Nen)
    Wareki +=  "." + str(Nensiki.month)
    Wareki +=  "." + str(Nensiki.day)

    return Wareki

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/car000/', MainHandler)
], debug=True)
