import sqlite3
from app.api.models.book import Book
from .author_data_adapter import AuthorsDataAdapter
from .resources_data_adapter import ResourcesDataAdapter
from .translator_data_adapter import TranslatorsDataAdapter
from .genre_data_adapter import GenresDataAdapter
from .language_data_adapter import LanguagesDataAdapter
from app.config import DB 
cn = sqlite3.connect(DB)
cur=cn.cursor()

class BooksDataAdapter:
    @staticmethod
    def get_all()->list:
        books=[]
        boks=cur.execute("SELECT * FROM books").fetchall()
        data_nn=cur.execute("SELECT id,name,title,description,esrb_rating_id,publisher_id,author_id,translator_id,resource_id,language_id,genre_id FROM books LEFT JOIN book_author ON books.id=book_author.book_id LEFT JOIN book_translator ON book_author.book_id=book_translator.book_id LEFT JOIN book_resource ON book_translator.book_id=book_resource.book_id LEFT JOIN book_language ON book_resource.book_id=book_language.book_id LEFT JOIN book_genre ON book_language.book_id=book_genre.book_id;").fetchall()
        resources=ResourcesDataAdapter.get_all()
        authors=AuthorsDataAdapter.get_all()
        translators=TranslatorsDataAdapter.get_all()
        genres=GenresDataAdapter.get_all()
        languages=LanguagesDataAdapter.get_all()
        for book in boks:
            res=[resource for id in set([dt[8] for dt in data_nn if dt[0]==book[0]]) for resource in resources if resource==id]
            aut=[author for id in set([dt[6] for dt in data_nn if dt[0]==book[0]]) for author in authors if author==id]
            tra=[translator for id in set([dt[7] for dt in data_nn if dt[0]==book[0]]) for translator in translators if translator==id]
            gen=[genre for id in set([dt[10] for dt in data_nn if dt[0]==book[0]]) for genre in genres if genre==id]
            lan=[language for id in set([dt[9] for dt in data_nn if dt[0]==book[0]]) for language in languages if language==id]

            books.append(Book(book[1],book[2],book[3],book[4],book[5],res,aut,tra,gen,lan,book[0]))
        
        return books
    @staticmethod
    def insert(book: Book) -> Book:

        try:

            # =========================
            # Insert Book
            # =========================

            sql = """
                INSERT INTO books
                (name, title, description, esrb_rating_id, publisher_id)
                VALUES (?, ?, ?, ?, ?)
            """

            cur.execute(
                sql,
                (
                    book.name,
                    book.title,
                    book.description,
                    book.esrb_rating.id if book.esrb_rating else None,
                    book.publisher.id if book.publisher else None
                )
            )

            book.id = cur.lastrowid


            # =========================
            # Authors
            # =========================

            for author in book.authors:

                cur.execute(
                    """
                    INSERT INTO book_author
                    (book_id, author_id)
                    VALUES (?, ?)
                    """,
                    (
                        book.id,
                        author.id
                    )
                )


            # =========================
            # Translators
            # =========================

            for translator in book.translators:

                cur.execute(
                    """
                    INSERT INTO book_translator
                    (book_id, translator_id)
                    VALUES (?, ?)
                    """,
                    (
                        book.id,
                        translator.id
                    )
                )


            # =========================
            # Resources
            # =========================

            for resource in book.resources:

                cur.execute(
                    """
                    INSERT INTO book_resource
                    (book_id, resource_id)
                    VALUES (?, ?)
                    """,
                    (
                        book.id,
                        resource.id
                    )
                )


            # =========================
            # Languages
            # =========================

            for language in book.languages:

                cur.execute(
                    """
                    INSERT INTO book_language
                    (book_id, language_id)
                    VALUES (?, ?)
                    """,
                    (
                        book.id,
                        language.id
                    )
                )


            # =========================
            # Genres
            # =========================

            for genre in book.genres:

                cur.execute(
                    """
                    INSERT INTO book_genre
                    (book_id, genre_id)
                    VALUES (?, ?)
                    """,
                    (
                        book.id,
                        genre.id
                    )
                )


            # Save everything
            cn.commit()

            return book


        except Exception:

            # If anything goes wrong,
            # undo all changes

            cn.rollback()

            raise
    @staticmethod
    def delete(id:int)->bool:
        if id in cur.execute("SELECT id FROM books"):
            cur.execute(f"DELETE FROM book_author where book_id={id}")

            cur.execute(f"DELETE FROM book_translator where book_id={id}")

            cur.execute(f"DELETE FROM book_resource where book_id={id}")

            cur.execute(f"DELETE FROM book_language where book_id={id}")

            cur.execute(f"DELETE FROM book_genre where book_id={id}")

            cur.execute(f"DELETE FROM books where id={id}")

            cn.commit()
            return True
        return False
    
    @staticmethod
    def search(title="", author="", translator="", publisher="", genre=""): 
        query = """ SELECT * FROM books
        LEFT JOIN publishers ON books.publisher_id = publishers.id
        LEFT JOIN book_author ON books.id = book_author.book_id
        LEFT JOIN authors ON book_author.author_id = authors.id
        LEFT JOIN book_translator ON books.id = book_translator.book_id
        LEFT JOIN translators ON book_translator.translator_id = translators.id
        LEFT JOIN book_genre ON books.id = book_genre.book_id
        LEFT JOIN genres ON book_genre.genre_id = genres.id WHERE 1=1 """
        if title:
            query += f" AND books.name LIKE '%{title}%'"
        if author:
            query += f" AND (authors.name LIKE '%{author}%' OR authors.last_name LIKE '%{author}%')"
        if translator:
            query += f" AND (translators.name LIKE '%{translator}%' OR translators.last_name LIKE '%{translator}%')"
        if publisher:
            query += f" AND publishers.name LIKE '%{publisher}%'"
        if genre:
            query += f" AND genres.name LIKE '%{genre}%'"
        rows = cur.execute(query).fetchall()
        books = []
        seen_ids = set()
        for row in rows:
            if row[0] not in seen_ids:
                seen_ids.add(row[0])
                books.append( Book( row[0], row[1], row[2], row[3], row[4], row[5], [], [], [], [], [] ) )
        return books 
    @staticmethod
    def update(book:Book):
        cur.execute(f"update books set name= '{book.name}'  where id= {book.id} ")
        cn.commit()
        print("تغییرات انجام شد.")



