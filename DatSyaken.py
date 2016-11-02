# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class DatSyaken(db.Model):
  SortNo          = db.IntegerProperty()                    # 車番
  Hizuke          = db.DateTimeProperty(auto_now_add=False) # 日付
  Kankaku         = db.IntegerProperty()                    # 車検間隔
  Biko            = db.StringProperty(multiline=False)      # 備考

  def GetSnap(self,SortNo):
    Sql =  "SELECT * FROM DatSyaken"
    Sql +=  " Where SortNo = :PSortNo"
    Sql += " Order By Hizuke Desc"
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    return Recs

  def GetNext(self,SortNo): # 次回車検日取得

    FontColor = ""

    Sql =  "SELECT * FROM DatSyaken"
    Sql +=  " Where SortNo = :PSortNo"
    Sql += " Order By Hizuke Desc"
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo)
    if Snap.count() == 0:
      return "",FontColor
    Recs = Snap.fetch(1)[0] # 最終レコード
    if Recs.Kankaku == "":
      return "",FontColor

    Next = str(Recs.Hizuke.year + Recs.Kankaku)
    Next += "/" + str(Recs.Hizuke.month) + "/" + str(Recs.Hizuke.day)

    NextDay = datetime.datetime.strptime(Next, '%Y/%m/%d')
    Kankaku =  NextDay - datetime.datetime.now()
    if Kankaku.days < 30:
      FontColor = ";background-color:red;color:white"
    elif Kankaku.days < 90:
      FontColor = ";background-color:yellow"
    
    return Next,FontColor
    
  def Delete(self,SortNo,Hizuke):
    Sql =  "SELECT * FROM DatSyaken"
    Sql += " Where SortNo = :PSortNo"
    Sql += "  And  Hizuke = :PHizuke" 
    Snap = db.GqlQuery(Sql)
    Snap.bind(PSortNo=SortNo,PHizuke=Hizuke)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return

  def GetRec(self,SortNo,Hizuke):
    Sql =  "SELECT * FROM DatSyaken"
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
