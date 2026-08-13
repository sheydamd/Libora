import sqlite3
from app.api.models.resource import Resource
from app.config import DB 
cn = sqlite3.connect(DB)
cur=cn.cursor()

class ResourcesDataAdapter:
    @staticmethod
    def get_all()->list:
        resources=[]
        resors=cur.execute("SELECT * FROM resources").fetchall()

        for resor in resors:
            resources.append(Resource(resor[1],resor[2],resor[3],resor[0]))
        return resources
    @staticmethod
    def insert(resource:Resource)->Resource:
        sql=f"INSERT INTO resources (title, type, establish_date) VALUES ('{resource.title}','{resource.type}','{resource.establish_date}')"
        cur.execute(sql)
        cn.commit()
        resource.id=cur.lastrowid
        return resource
    @staticmethod
    def delete(id:int)->bool:
        if id not in cur.execute("SELECT resource_id FROM book_resource"):
            cur.execute(f"DELETE FROM resources where id={id}")
            cn.commit()
            return True
        return False
    @staticmethod
    def search(title:str):
        resources=[]
        auths=cur.execute(f"SELECT * FROM resources  where title like '%{title}%'").fetchall()
        for auth in auths:
            resources.append(Resource(auth[0],auth[1],auth[2],auth[3]))
        return resources
    @staticmethod
    def update(resource: Resource):

        cur.execute(
            """
            UPDATE resources
            SET title = ?,
                type = ?,
                establish_date = ?
            WHERE id = ?
            """,
            (
                resource.title,
                resource.type,
                resource.establish_date,
                resource.id
            )
        )

        cn.commit()
        print("تغییرات انجام شد.")

