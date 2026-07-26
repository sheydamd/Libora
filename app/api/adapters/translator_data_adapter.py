import sqlite3
from app.api.models.translator import Translator
from app.config import DB 
cn = sqlite3.connect(DB)
cur=cn.cursor()

class TranslatorsDataAdapter:
    @staticmethod
    def get_all()->list:
        translators=[]
        transls=cur.execute("SELECT * FROM translators").fetchall()

        for transl in transls:
            translators.append(Translator(transl[0],transl[1],transl[2],transl[3],transl[4]))
        return translators
    @staticmethod
    def insert(translator:Translator)->Translator:
        sql=f"INSERT INTO translators (national_code, name, last_name, birthday, grade) VALUES ('{translator.national_code}','{translator.name}','{translator.last_name}','{translator.birthday}','{translator.grade}')"
        cur.execute(sql)
        cn.commit()
        translator.id=cur.lastrowid
        return translator    
    @staticmethod
    def delete(id:int)->bool:
        if id not in cur.execute("SELECT translator_id FROM book_translator"):
            cur.execute(f"DELETE FROM translators where id={id}")
            cn.commit()
            return True
        return False
    
    @staticmethod
    def search(name:str,last_name:str):
        translators=[]
        auths=cur.execute(f"SELECT * FROM translators  where name like '%{name}%' AND last_name like '%{last_name}%'").fetchall()
        for auth in auths:
            translators.append(Translator(auth[0],auth[1],auth[2],auth[3],auth[4]))
        return translators
    @staticmethod
    def update(translator:Translator):
        cur.execute(f"update translatorss set name= '{translator.name}'  where id= {translator.id} ")
        cn.commit()
        print("تغییرات انجام شد.")
