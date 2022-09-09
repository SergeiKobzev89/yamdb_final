import csv
import sqlite3

from date import datetime as dt


conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

with open("../static/data/category.csv", "r", encoding="utf8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            "INSERT INTO yamdb_category "
            "(id, name, slug) "
            "VALUES(?, ?, ?)",
            (id, name, slug)
        )
        conn.commit()

with open("../static/data/comments.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        review_id = row['review_id']
        text = row['text']
        author_id = row['author']
        pub_date = row['pub_date']
        c.execute(
            "INSERT INTO yamdb_comment "
            "(id, text, pub_date, author_id, review_id) "
            "VALUES(?, ?, ?, ?, ?)",
            (id, text, pub_date, author_id, review_id)
        )
        conn.commit()

with open("../static/data/genre.csv", "r", encoding="utf8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            "INSERT INTO yamdb_genre "
            "(id, name, slug) "
            "VALUES(?, ?, ?)",
            (id, name, slug)
        )
        conn.commit()

with open("../static/data/genre_title.csv", "r", encoding="utf8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        title_id = row['title_id']
        genre_id = row['genre_id']
        c.execute(
            "INSERT INTO yamdb_title_genre"
            "(id, title_id, genre_id) "
            "VALUES(?, ?, ?)",
            (id, title_id, genre_id)
        )
        conn.commit()

with open("../static/data/review.csv", "r", encoding="utf8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        title_id = row['title_id']
        text = row['text']
        author_id = row['author']
        score = row['score']
        pub_date = row['pub_date']
        c.execute(
            "INSERT INTO yamdb_review "
            "(id, text, score, pub_date, author_id, title_id) "
            "VALUES(?, ?, ?, ?, ?, ?)",
            (id, text, score, pub_date, author_id, title_id)
        )
        conn.commit()

with open("../static/data/titles.csv", "r", encoding="utf8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        year = row['year']
        category_id = row['category']
        c.execute(
            "INSERT INTO yamdb_title "
            "(id, name, year, category_id) "
            "VALUES(?, ?, ?, ?)",
            (id, name, year, category_id)
        )
        conn.commit()

with open("../static/data/users.csv", "r", encoding="utf8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        password = '12345678'
        username = row['username']
        email = row['email']
        role = row['role']
        bio = row['description']
        first_name = row['first_name']
        last_name = row['last_name']
        date_joined = dt.now()
        if role == 'user':
            is_superuser = False
            is_staff = False
            is_active = True
        elif role == 'moderator':
            is_superuser = False
            is_staff = True
            is_active = True
        elif role == 'admin':
            is_superuser = True
            is_staff = False
            is_active = True
        c.execute(
            "INSERT INTO api_user "
            "(id, password, username, email, role, bio, first_name, "
            "last_name, is_superuser, is_staff, is_active, date_joined) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (id, password, username, email, role, bio, first_name,
             last_name, is_superuser, is_staff, is_active, date_joined)
        )
        conn.commit()

conn.close()
