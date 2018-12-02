import os
import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/index')
def index():
    urls = {'анкета (пройдено, но можно еще раз)': url_for('data'),
            'Ваши результаты (json)': url_for('resres'),
            'Все результаты': url_for('stats'),
            'просто стихи застряли в голове': url_for('poem'),}
    return render_template('index.html', urls=urls)

@app.route('/json')
def resres():
    with open(r'''C:\Users\Дарья\Desktop\project\data.csv''', encoding="Windows-1251") as f:
        ans = f.read().split('\n')
    for a in range(len(ans)):
        ans[a] = ans[a].split(';')
    all_keys = ['Имя', 'Возраст', 'Место рождения', 'Ведущий', 'Камень-ножницы-бумага', 'Любимая игра']
    results = {}
    n = -1
    for i in range(len(all_keys)):
        n += 1
        results[str(all_keys[i])] = []    
        results[str(all_keys[i])].append(ans[a][n])
    with open(r'''C:\Users\Дарья\Desktop\project\found.json''', 'w', encoding='utf-16') as f:
        res = json.dumps(results, ensure_ascii = False)
        f.write(res)
    with open(r'''C:\Users\Дарья\Desktop\project\found.json''', encoding='utf-16') as f:
        content = f.read().split('\n')
    return render_template('json.html', content=content)


@app.route('/stats')
def stats():
    with open(r'''C:\Users\Дарья\Desktop\project\data.csv''', encoding="Windows-1251") as f:
        ans = f.read().split('\n')
    for i in range(len(ans)):
        ans[i] = ans[i].split(';')
    return render_template('stats.html', ans=ans, num=range(len(ans)), h=range(len(ans[2])))

@app.route('/')
def data():
    if request.args:
        name = str(request.args['name'])
        age = str(request.args['age'])
        place = str(request.args['place'])
        st = True if 'student' in request.args else False
        with open(r'''C:\Users\Дарья\Desktop\project\data.csv''', 'a', encoding="Windows-1251") as f:
            f.write('\n' + name  + ';' + age  + ';' + place  + ';')
        return redirect (url_for('radio'))
    return render_template('data.html')
        
@app.route('/radio')
def radio():
    if request.args:
        chosen = str(request.args['chosen'])
        cuefa = str(request.args['cuefa'])
        with open(r'''C:\Users\Дарья\Desktop\project\data.csv''', 'a', encoding="Windows-1251") as f:
            f.write(chosen  + ';' + cuefa  + ';')
        return redirect (url_for('quest'))
    return render_template('radio.html')



@app.route('/quest')
def quest():
    if request.args:
        quest = str(request.args['quest'])
        with open(r'''C:\Users\Дарья\Desktop\project\data.csv''', 'a', encoding="Windows-1251") as f:
            f.write(quest)
        return render_template ('thanks.html')
    return render_template('quest.html')


@app.route('/thanks')
def thanks():
    if request.args:
        quest = request.args['quest']
        return render_template('thanks.html', quest=quest)
    return render_template('quest.html')


@app.route('/poem')
def poem():
    with open(r'''C:\Users\Дарья\Desktop\project\poem.txt.txt''', encoding='UTF-8') as f:
        content = f.read().split('\n')
    return render_template("poem.html", content=content)

if __name__ == '__main__':
    app.run(debug=True)
