import sqlite3
import random
from faker import Faker

conn = sqlite3.connect('data.db')
fake = Faker()
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS authors(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    SAXELI TEXT NOT NULL,
    GVARI TEXT NOT NULL,
    DAB_TARIGI TEXT NOT NULL,
    DAB_ADGILI TEXT NOT NULL
    )


''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DASAXELEBA TEXT NOT NULL,
    KATEGORIIS_DASAXELEBA TEXT NOT NULL,
    GVERDEBIS_RAODENOBA INTEGER NOT NULL,
    GAMOCEMIS_TARIGI TEXT NOT NULL,
    AVTORIS_ID INTEGER NOT NULL,
    FOREIGN KEY (AVTORIS_ID) REFERENCES authors (ID)


    )


''')

authors_data = []
for i in range(500):
    name = fake.name()
    name1 = name.find(" ")
    surname = name[name1 + 1:]
    name2 = name[:name1]
    place = fake.city()
    date = fake.date_of_birth().strftime('%Y-%m-%d')
    authors_data.append((name2, surname, date, place))

cursor.executemany("INSERT INTO authors (SAXELI, GVARI,DAB_TARIGI,DAB_ADGILI) "
                   "VALUES (?, ?,?,?)", authors_data)

author_ids = [author_id[0] for author_id in cursor.execute('''SELECT ID FROM authors''').fetchall()]
books_data = []
for i in range(1000):
    dasaxeleba = fake.sentence(nb_words=3)
    kategoria = fake.word(ext_word_list=['Fiction', 'Non-Fiction', 'Science',
                                         'Fantasy', 'History', 'Biography'])
    gverdebi = random.randint(100, 1000)
    tarigi = fake.date_this_century()
    id_of_author = random.choice(author_ids)
    books_data.append((dasaxeleba, kategoria, gverdebi, tarigi, id_of_author))

cursor.executemany("INSERT INTO books (DASAXELEBA, KATEGORIIS_DASAXELEBA,GVERDEBIS_RAODENOBA"
                   ",GAMOCEMIS_TARIGI,AVTORIS_ID ) "
                   "VALUES (?, ?,?,?,?)", books_data)

cursor.execute('''
    SELECT * FROM books
    ORDER BY GVERDEBIS_RAODENOBA DESC
    LIMIT 1
''')
book_with_most_pages = cursor.fetchone()
print(f"წიგნი ყველაზე მეტი გვერდებით:\nაიდი: {book_with_most_pages[0]}\nდასახელება: {book_with_most_pages[1]}"
      f"\nკატეგორია: {book_with_most_pages[2]}\nგვერდების რაოდენობა: {book_with_most_pages[3]}\n"
      f"გამოშვების თარიღი: {book_with_most_pages[4]}\nავტორის აიდი: {book_with_most_pages[5]}\n"
      f"-------------------------------------")

cursor.execute('''SELECT AVG(GVERDEBIS_RAODENOBA) FROM books''')
avg = cursor.fetchone()[0]
print(f"წიგნების საშუალო გვერდების რაოდენობაა: {avg}\n"
      f"-------------------------------------")

cursor.execute('''SELECT SAXELI, GVARI  FROM authors ORDER BY DAB_TARIGI DESC LIMIT 1''')
young_author = cursor.fetchone()
print(f"ყველაზე ახალგაზრდა ავტორია: {young_author[0]} {young_author[1]}\n"
      f"-------------------------------------")

cursor.execute('''
    SELECT SAXELI,GVARI FROM authors
    WHERE ID NOT IN (SELECT AVTORIS_ID FROM books)
''')
authors_without_books = cursor.fetchall()

print('ავტორები წიგნების გარეშე: ')
for i in range(len(authors_without_books)):
    print(f"{authors_without_books[i][0]} {authors_without_books[i][1]} ")
print('-------------------------------------')

cursor.execute('''
    SELECT a.SAXELI, a.GVARI, COUNT(b.ID) AS book_count
    FROM authors a
    JOIN books b ON a.ID = b.AVTORIS_ID
    GROUP BY a.ID
    HAVING book_count > 3

''')
authors_with_more_than_3_books = cursor.fetchall()

print("ავტორები 3-ზე მეტი წიგნით:")
for i in range(len(authors_with_more_than_3_books)):
    print(f'{authors_with_more_than_3_books[i][0]} {authors_with_more_than_3_books[i][1]} |'
          f' წიგნი: {authors_with_more_than_3_books[i][2]}  ')

conn.commit()
conn.close()