import sqlite3
from app.api.models.author import Author
from app.config import DB 
cn = sqlite3.connect(DB)
cur=cn.cursor()

class AuthorsDataAdapter:
    @staticmethod
    def get_all() -> list:
        authors = []
        auths = cur.execute("SELECT * FROM authors").fetchall()

        for auth in auths:
            authors.append(
                Author(
                    auth[1],  # national_code
                    auth[2],  # name
                    auth[3],  # last_name
                    auth[4],  # birthday
                    auth[5],  # grade
                    auth[0]   # id
                )
            )

        return authors
    @staticmethod
    def insert(author:Author)->Author:
        sql=f"INSERT INTO authors (national_code, name, last_name, birthday, grade) VALUES ('{author.national_code}','{author.name}','{author.last_name}','{author.birthday}','{author.grade}')"
        cur.execute(sql)
        cn.commit()
        author.id=cur.lastrowid
        return author   
    @staticmethod
    def delete(id:int)->bool:
        if id in cur.execute("SELECT id FROM books"):
            cur.execute(f"DELETE FROM authors where id={id}")
            cn.commit()
            return True
        return False
    @staticmethod
    def search(name:str,last_name:str):
        authors=[]
        auths=cur.execute(f"SELECT * FROM authors  where name like '%{name}%' AND last_name like '%{last_name}%'").fetchall()
        for auth in auths:
            authors.append(Author(auth[0],auth[1],auth[2],auth[3],auth[4],auth[5]))
        return authors
    @staticmethod
    def update(author:Author):
        cur.execute(f"update authors set name= '{author.name}'  where id= {author.id} ")
        cn.commit()
        print("تغییرات انجام شد.")
