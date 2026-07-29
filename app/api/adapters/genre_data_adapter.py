import sqlite3
from app.api.models.genre import Genre
from app.config import DB 
cn = sqlite3.connect(DB)
cur=cn.cursor()

class GenresDataAdapter:
    @staticmethod
    def get_all()->list:
        genres=[]
        gen=cur.execute("SELECT * FROM genres").fetchall()

        for genrese in gen:
            genres.append(Genre(genrese[1],genrese[0]))
        return genres
    @staticmethod
    def insert(genre:Genre)->Genre:
        sql=f"INSERT INTO genres (name) VALUES ('{genre.name}')"
        cur.execute(sql)
        cn.commit()
        genre.id=cur.lastrowid
        return genre  
    @staticmethod
    def delete(id:int)->bool:
        if id not in cur.execute("SELECT genre_id FROM book_genre"):
            cur.execute(f"DELETE FROM genres where id={id}")
            cn.commit()
            return True
        return False
    @staticmethod
    def search(name:str):
        genres=[]
        auths=cur.execute(f"SELECT * FROM genres  where name like '%{name}%'").fetchall()
        for auth in auths:
            genres.append(Genre(auth[0],auth[1]))
        return genres
    @staticmethod
    def update(genre:Genre):
        cur.execute(f"update genres set name= '{genre.name}'  where id= {genre.id} ")
        cn.commit()
        print("تغییرات انجام شد.")
 