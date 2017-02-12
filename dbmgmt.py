import sqlite3

conn = sqlite3.connect("example.db")
c = conn.cursor()
#c.execute('''CREATE TABLE stickers (id int, img text, author text, name text)''')
#c.execute("INSERT INTO stickers VALUES(1, 'PRIVET', 'https://heusosina\\kek.html', 'your mom')")
#conn.commit()
for i in c.execute("SELECT * FROM stickers WHERE id = 31").fetchone():
    print(i)
conn.close