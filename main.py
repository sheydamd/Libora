from app.api.models.book import Book
from app.api.models.author import Author
from app.api.models.esrb import Esrb
from app.api.models.publisher import Publisher
from app.api.models.resource import Resource
from app.api.models.translator import Translator
from app.api.models.genre import Genre
from app.api.models.language import Language
from app.api.adapters.book_data_adapter import BooksDataAdapter
esrb=Esrb(id=1,name="g"),
publisher=Publisher(id=1,name="a",address="la",phone_number="090",fax_number="123",email="sheyda",establish_date="1405"),
resource=Resource(id=1,title="A",type="roman",establish_date="123"),
author=Author(id=1,national_code="031",name="hassan",last_name="hassani",birthday="12",grade="3"),
translator=Translator(id=1,national_code=" ",name=" ",last_name=" ",grade=" "),
genre=Genre(id=1,name=" "),
language=Language(id=1,name=" ")
b1=Book(id=1,
        name=" ",
        title=" ",
        description=" ",
        esrb_rating=esrb,
        publisher=publisher,
        resources=[resource],
        authors=[author],
        translators=[translator],
        genres=[genre],
        languages=[language])

bookad=BooksDataAdapter()
