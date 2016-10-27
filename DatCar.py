# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class DatCar(db.Model):
  SortNo          = db.IntegerProperty()                    # 連番
  CarNo           = db.StringProperty(multiline=False)      # 車両番号
  SyozaiCD        = db.IntegerProperty()                    # 所在CD
  Syozai          = db.StringProperty(multiline=False)      # 所在!非正規化
  MakerCD         = db.IntegerProperty()                    # メーカCD
  Maker           = db.StringProperty(multiline=False)      # メーカ!非正規化
  SyasyuCD        = db.IntegerProperty()                    # 車種CD
  Syasyu          = db.StringProperty(multiline=False)      # 車種!非正規化
  SyaryoCD        = db.IntegerProperty()                    # 車両CD
  Syaryo          = db.StringProperty(multiline=False)      # 車両!非正規化
  Nensiki         = db.DateTimeProperty(auto_now_add=False) # 年式
  LastSyaken      = db.DateTimeProperty(auto_now_add=False) # 前回車検
  SyakenKankaku   = db.IntegerProperty()                    # 車検間隔
  Biko            = db.StringProperty(multiline=False)      # 備考
  YukoFlg         = db.BooleanProperty()                    # 有効フラグ
  HaisyaBi        = db.DateTimeProperty(auto_now_add=False) # 廃車日

  def GetAll(self):

    Sql =  "SELECT * FROM DatCar"
    Sql += " Order By SortNo,CarNo"

    Snap = db.GqlQuery(Sql)
  
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())

    return Recs
