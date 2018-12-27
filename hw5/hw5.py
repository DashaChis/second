import sqlite3
import re
from flask import Flask
from flask import render_template, request, url_for, redirect   

def looking_for_freedom(word):
    word = '\'%{' + word + '%\''
    content = []
    url = []
    conn = sqlite3.connect('tumentoday.db')
    c = conn.cursor()
    for row in c.execute('SELECT url, content FROM data WHERE content LIKE ' + word):
        url.append(row[0])
        content.append(row[1][0:200])
    return content, url

app = Flask(__name__)
@app.route('/')
def index():
    if request.args:
        word = str(request.args['word'])
        content, url = looking_for_freedom(word)
        return render_template('got_it.html', amount=range(len(content)), url=url, content=content)
    return render_template('index.html')


def stuck_in_the_tables():
    with open(r'''C:\Users\Asus\Desktop\tumentoday\metadata.csv''', encoding='Windows-1251') as f:
        text = f.read()
    words = text.split('\n')
    conn = sqlite3.connect('tumentoday.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data(url TEXT, author TEXT, year TEXT, content TEXT)')
    for i in range(len(words)-1):
        words[i] = words[i].split(';')
        url = words[i][10]
        author = words[i][1]
        year = words[i][3]
        path = str(words[i][0])
        with open(path, encoding='utf-8') as f:
            text = f.read()
            text = (re.sub('@.+','', text)).replace('\t', '')
            text = text.replace('\n', '')
        c = conn.cursor()
        c.execute('INSERT INTO data VALUES (?, ?, ?, ?)', (url, author, year, text))
        conn.commit()
    conn.close()


def main():
    stuck_in_the_tables()
                 
if __name__ == '__main__':
    main()
    app.run(debug=False)
