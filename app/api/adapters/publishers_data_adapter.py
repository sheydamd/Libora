import sqlite3
from app.api.models.publisher import Publisher
from app.config import DB 
cn = sqlite3.connect(DB)
cur=cn.cursor()

class PublishersDataAdapter:
    @staticmethod
    def get_all()->list:
        publishers=[]
        puplis=cur.execute("SELECT * FROM publishers").fetchall()

        for pupli in puplis:
            publishers.append(Publisher(pupli[1],pupli[2],pupli[3],pupli[4],pupli[5],pupli[6],pupli[0]))
        return publishers
    @staticmethod
    def insert(publisher:Publisher)->Publisher:
        sql=f"INSERT INTO publishers (name, address, phone_number, fax_number, email, establish_date) VALUES ('{publisher.name}','{publisher.address}','{publisher.phone_number}','{publisher.fax_number}','{publisher.email}','{publisher.establish_date}')"
        cur.execute(sql)
        cn.commit()
        publisher.id=cur.lastrowid
        return publisher    
    @staticmethod
    def delete(id:int)->bool:
        if id not in cur.execute("SELECT publisher_id FROM books"):
            cur.execute(f"DELETE FROM publishers where id={id}")
            cn.commit()
            return True
        return False
    @staticmethod
    def search(name:str):
        publishers=[]
        pubs=cur.execute(f"SELECT * FROM publishers  where name like '%{name}%'").fetchall()
        for pu in pubs:
            publishers.append(Publisher(pu[0],pu[1],pu[2],pu[3],pu[4],pu[5],pu[6]))
        return publishers
    @staticmethod
    def update(publisher:Publisher):
        cur.execute(f"update publishers set name= '{publisher.name}'  where id= {publisher.id} ")
        cn.commit()
        print("تغییرات انجام شد.")

