import sqlite3
from app.api.models.esrb import Esrb
from app.config import DB 
cn = sqlite3.connect(DB)
cur=cn.cursor()

class EsrbsDataAdapter:
    @staticmethod
    def get_all()->list:
        esrbs=[]
        esrbses=cur.execute("SELECT * FROM esrb_ratings").fetchall()
        for row in esrbses:
            esrbs.append(
                Esrb(row[1], row[0])
            )
        return esrbs
    
    @staticmethod
    def insert(esrb:Esrb)->Esrb:
        sql=f"INSERT INTO esrb_ratings (esrb_name) VALUES ('{esrb.name}')"
        cur.execute(sql)
        cn.commit()
        esrb.id=cur.lastrowid
        return esrb 
    
    @staticmethod
    def delete(id:int)->bool:
        if id not in cur.execute("SELECT esrb_rating_id FROM books"):
            cur.execute(f"DELETE FROM esrb_ratings where id={id}")
            cn.commit()
            return True
        return False
    
    @staticmethod
    def search(esrb_name:str):
        esrbs=[]
        auths=cur.execute(f"SELECT * FROM esrb_ratings  where name like '%{esrb_name}%'").fetchall()
        for auth in auths:
            esrbs.append(Esrb(auth[0],auth[1]))
        return esrbs
    @staticmethod
    def update(esrbs:Esrb):
        cur.execute(f"update esrb_ratings set name= '{esrbs.name}'  where id= {esrbs.id} ")
        cn.commit()
        print("تغییرات انجام شد.")

