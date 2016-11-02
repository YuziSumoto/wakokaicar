# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import datetime

class MstSyozai(db.Model):
  Code            = db.IntegerProperty()                    # ＣＤ
  Name            = db.StringProperty(multiline=False)      # 名称

  def GetAll(self):
    Sql =  "SELECT * FROM MstSyozai"
    Sql += " Order By Code"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(Snap.count())
    return Recs

  def GetRec(self,Code):
    Sql =  "SELECT * FROM MstSyozai"
    Sql += " Where Code = " + str(Code)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Recs = {}
    else:
      Recs = Snap.fetch(1)[0]
    return Recs

  def Delete(self,Code): # レコード削除
    Sql =  "SELECT * FROM MstSyozai"
    Sql += " Where Code = " + Code
    Snap = db.GqlQuery(Sql)
    for Rec in Snap.fetch(Snap.count()):
      Rec.delete()
    return
  
  def Add(self,Code,Name):

    self.Delete(Code) # 既存削除

    AddRec = MstSyozai() # 新規レコード
    AddRec.Code = int(Code)
    AddRec.Name = Name
    AddRec.put() # 保存

    return
