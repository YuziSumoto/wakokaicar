# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class DatUse(db.Model):
  SortNo          = db.IntegerProperty()                    # 車番
  Hizuke          = db.DateTimeProperty(auto_now_add=False) # 日付
  STime           = db.DateTimeProperty(auto_now_add=False) # 出庫時刻
  ETime           = db.DateTimeProperty(auto_now_add=False) # 入庫時刻
  Ikisaki         = db.StringProperty(multiline=False)      # 行き先
  Mokuteki        = db.StringProperty(multiline=False)      # 運行目的
  Unten           = db.StringProperty(multiline=False)      # 運転者
  Douzyo          = db.StringProperty(multiline=False)      # 同乗者
  Kyori           = db.IntegerProperty()                    # 終業時メータ
  Biko            = db.StringProperty(multiline=False)      # 備考

  def GetSnap(self,SortNo):
    Sql =  "SELECT * FROM DatUse"
    Sql +=  " Where SortNo = :PSortNo"
    Sql += " Order By Hizuke Desc,STime Desc"
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    return Recs

  def GetKyori(self,SortNo): # 最終使用距離取得
    Sql =  "SELECT * FROM DatUse"
    Sql +=  " Where SortNo = :PSortNo"
    Sql += " Order By Kyori Desc"
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo)
    if Snap.count() == 0:
      return "",0
    Recs = Snap.fetch(1)[0] # 最終レコード
    if Recs.Kyori is None:
      return "",0
    return Recs.Hizuke,Recs.Kyori
    
  def Delete(self,SortNo,Hizuke,STime):
    Sql =  "SELECT * FROM DatUse"
    Sql += " Where SortNo = :PSortNo"
    Sql += "  And  Hizuke = :PHizuke" 
    Sql += "  And  STime  = :PSTime" 
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo,PHizuke=Hizuke,PSTime=STime)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def GetRec(self,SortNo,Hizuke,STime):
    Sql =  "SELECT * FROM DatUse"
    Sql += " Where SortNo = :PSortNo"
    Sql += "  And  Hizuke = :PHizuke" 
    Sql += "  And  STime  = :PSTime" 
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo,PHizuke=Hizuke,PSTime=STime)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(1)[0]

    return Recs

  def AddRec(self,Rec):
    self.Delete(Rec.SortNo,Rec.Hizuke,Rec.STime)
    Rec.put()
    return 
