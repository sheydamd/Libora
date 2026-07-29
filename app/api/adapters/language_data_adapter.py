import sqlite3
from app.api.models.language import Language
from app.config import DB 
cn = sqlite3.connect(DB)
cur=cn.cursor()

class LanguagesDataAdapter:
    @staticmethod
    def get_all()->list:
        Languages=[]
        Langs=cur.execute("SELECT * FROM languages").fetchall()

        for Lang in Langs:
            Languages.append(Language(Lang[1],Lang[0]))
        return Languages
    @staticmethod
    def insert(language:Language)->Language:
        sql=f"INSERT INTO esrb_ratings (name) VALUES ('{language.name}')"
        cur.execute(sql)
        cn.commit()
        language.id=cur.lastrowid
        return language 
    @staticmethod
    def delete(id:int)->bool:
        if id not in cur.execute("SELECT language_id FROM book_language"):
            cur.execute(f"DELETE FROM languages where id={id}")
            cn.commit()
            return True
        return False
    
    @staticmethod
    def search(name:str):
        languages=[]
        auths=cur.execute(f"SELECT * FROM authors  where name like '%{name}%'").fetchall()
        for auth in auths:
            languages.append(Language(auth[0],auth[1]))
        return languages
    @staticmethod
    def update(language:Language):
        cur.execute(f"update languages set name= '{language.name}'  where id= {language.id} ")
        cn.commit()
        print("تغییرات انجام شد.")
