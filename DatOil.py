# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class DatOil(db.Model):
  SortNo          = db.IntegerProperty()                    # 車番
  Hizuke          = db.DateTimeProperty(auto_now_add=False) # 日付
  Kyori           = db.IntegerProperty()                    # 距離
  Element         = db.IntegerProperty()                    # エレメント
  Biko            = db.StringProperty(multiline=False)      # 備考

  def GetSnap(self,SortNo):
    Sql =  "SELECT * FROM DatOil"
    Sql +=  " Where SortNo = :PSortNo"
    Sql += " Order By Hizuke Desc"
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    return Recs

  def GetNext(self,SortNo): # 次回交換距離取得
    Sql =  "SELECT * FROM DatOil"
    Sql +=  " Where SortNo = :PSortNo"
    Sql += " Order By Hizuke Desc"
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo)
    if Snap.count() == 0:
      return 0
    Recs = Snap.fetch(1)[0] # 最終レコード
    if Recs.Kyori is None:
      return 0
    return Recs.Kyori + 5000
    
  def Delete(self,SortNo,Hizuke):
    Sql =  "SELECT * FROM DatOil"
    Sql += " Where SortNo = :PSortNo"
    Sql += "  And  Hizuke = :PHizuke" 
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo,PHizuke=Hizuke)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def GetRec(self,SortNo,Hizuke):
    Sql =  "SELECT * FROM DatOil"
    Sql += " Where SortNo = :PSortNo"
    Sql += "  And  Hizuke = :PHizuke" 
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo,
              PHizuke=Hizuke)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(1)[0]

    return Recs

  def AddRec(self,AddRec):
    self.Delete(AddRec.SortNo,AddRec.Hizuke)
    AddRec.put()
    return 
