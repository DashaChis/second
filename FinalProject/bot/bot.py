import markovify  
import urllib.request
import json
import re
from flask import Flask, render_template, request

def wall_requst(offset):
    token = '4e6f5f194e6f5f194e6f5f19ad4e044b6044e6f4e6f5f191290f18a063374014f7fdafe'
    version = '5.92'
    group = '-28122932'
    count = '100'
    posts = ''
    req = urllib.request.Request(
        'https://api.vk.com/method/wall.get?owner_id=%s&offset=%s&count=%s&v=%s&access_token=%s'
        % (group, offset, count, version, token))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)  
    #print(data)
    for i in range(len(data['response']['items'])):
        posts = posts + '\n' + data['response']['items'][i]['text']
    return posts

def wr():  
    with open('p.txt', 'w', encoding='utf-8') as f:
        pass
    for i in range(1, 2001, 100):
        perawki = wall_requst(i)
        result = re.sub(r'[©\[].*','', perawki)  
        perawki = re.sub(r'\n{2,5}', '\n', result)  
        with open('p.txt', 'a', encoding='utf-8') as f:
            f.write(perawki)
        with open('p.txt', 'r', encoding='utf-8') as f:
            newtxt = ''
            for line in f:
                if len(line.split()) <= 9 and len(re.findall(r'[\d\\]', line)) == 0:  
                    newtxt = newtxt + line
        with open('p.txt', 'w', encoding='utf-8') as f:
            f.write(newtxt)

def check_syl(st, num):  
    vow = ['а', 'о', 'э', 'ы', 'и', 'ю', 'я', 'е', 'ё', 'у']
    v = 0
    if st != None:
        for letter in st:
            if letter in vow:
                v += 1
        if v == num:
            return 'OK'  
    else:
        return 'NO'  

def wr_str():  
    first_third = ''
    second_last = ''
    with open('p.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if check_syl(line, 9) == 'OK':  
                first_third = first_third + line
            elif check_syl(line, 8) == 'OK': 
                second_last = second_last + line
    with open('first.txt', 'w', encoding='utf-8') as f:
        f.write(first_third)
    with open('second.txt', 'w', encoding='utf-8') as f:
        f.write(second_last)

def make_model():  
    with open('first.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    model_1_3 = markovify.NewlineText(text)
    with open('second.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    model_2_4 = markovify.NewlineText(text)
    return model_1_3, model_2_4

def gen_str(word, m, s2='', isWord=False, syl=9, turns=100):
    t = 0
    s1 = ''
    if not isWord:  
        while check_syl(s1, syl) != 'OK' or s1 == s2:  
            s1 = m.make_sentence_with_start(word, strict=False, tries=30)  
            t += 1
            if t == turns:  
                break
        if t == turns: 
            word = ' ' + word
            t = 0
            while check_syl(s1, syl) != 'OK' or word not in s1 or s1 == s2:
                s1 = m.make_sentence(tries=30)  
                t += 1
                if t == turns:
                    break
            if t == turns: 
                while check_syl(s1, syl) != 'OK' or s1 == s2:  
                    s1 = m.make_sentence(tries=30)
                return s1, isWord
            else:  
                isWord = True
                return s1, isWord
        else:  
            isWord = True
            return s1, isWord
    else:
        while check_syl(s1, syl) != 'OK' or s1 == s2:
            s1 = m.make_sentence(tries=30)
        return s1, isWord

def gen_pir(word):
    m1, m2 = make_model()
    isWord = False
    so, isWord = gen_str(word, m1, isWord=isWord)
    ss, isWord = gen_str(word, m2, isWord=isWord, syl=8)
    st, isWord = gen_str(word, m1, s2=so, isWord=isWord)  
    sf, isWord = gen_str(word, m2, s2=ss, isWord=isWord, syl=8)
    pirow = so + '\n' + ss + '\n' + st + '\n' + sf
    return pirow, isWord

def main():
    wr()
    wr_str()

app = Flask(__name__)  

@app.route('/')
def index():
    main()
    if request.args:
        wrd = str(request.args['word'])
        resp, isWord = gen_pir(wrd)
        resp = resp.split('\n')
        return render_template('result.html',isWord=isWord, resp=resp)
    return render_template('index.html')

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
