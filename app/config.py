import os
APP_DIR=os.path.dirname(
    os.path.abspath(__file__)
)
DB=os.path.join(
    APP_DIR,
    "database",
    "books.db"
)