import json
import urllib.request

def your_choice():
    list_of_us = ['elmiram', 'maryszmary', 'lizaku', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'agricolamz', 'lehkost', 'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham', 'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
    print("Выберите пользователя из списка и введите его ник: elmiram, maryszmary, lizaku, nevmenandr, ancatmara, roctbb, akutuzov, agricolamz, lehkost, kylepjohnson, mikekestemont, demidovakatya, shwars, JelteF, timgraham, arogozhnikov, jasny, bcongdon, whyisjake, gvanrossum")
    user = input()
    while user not in list_of_us:
        print ("Пожалуйста, введите имя из списка!")
        user = input()
    print("Вы выбрали пользователя ", user)
    return user

def names_descriptions(user):
    token = "f9030b5598a0406ec00c847e45e4a1cd2cbd383f"
    url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user, token)
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    data = json.loads(text)
    print("Вот список его репозиториев и описания к ним: ")
    for i in data:
        ans = '{}: {}'.format(i["name"], i["description"]) 
 #       print(i["name"])
  #      print(i["description"])
        print(ans)
    return user

def lang(user):
    token = "f9030b5598a0406ec00c847e45e4a1cd2cbd383f"
    url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user, token)
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    data = json.loads(text)
    lang = []
    for i in data:
        lang.append(i["language"])
    ans = {}
    a, an = None, 0
    for i in lang:
        ans[i] = t = ans.get(i, 0) + 1
        if t > an:
            a, an = i, t
    print("Для каждого языка указано количество репозиториев, где он используется:")
    print(ans)

def rep(list_of_us):
    a = 0
    b = 0
    for i in list_of_us:
        user = i
        token = "f9030b5598a0406ec00c847e45e4a1cd2cbd383f"
        url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user, token)
        response = urllib.request.urlopen(url)
        text = response.read().decode('utf-8')
        data = json.loads(text)
        a = len(data)
        if b < a:
            b = a
            big_bro = [user]
        elif b == a:
            big_bro.append(user)
    print("Среди заданных в списке пользователей максимальное количество репозиториев - ", b, ", больше всего репозиториев у ", big_bro, b)

def zaban(list_of_us):
    all_z = []
    for i in list_of_us:
        user = i
        token = "f9030b5598a0406ec00c847e45e4a1cd2cbd383f"
        url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user, token)  
        response = urllib.request.urlopen(url)
        text = response.read().decode('utf-8')
        data = json.loads(text)
        for user in data:
            all_z.append(user["language"])
    elems = {}
    e, em = None, 0
    for i in all_z:
        elems[i] = t = elems.get(i, 0) + 1
        if t > em:
            e, em = i, t
    print("Среди всех пользователей чаще всего встречается язык ",e)


        
def main():
    list_of_us = ['elmiram', 'maryszmary', 'lizaku', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'agricolamz', 'lehkost', 'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham', 'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
    lang(names_descriptions(your_choice()))
    rep(list_of_us)
    zaban(list_of_us)

if __name__ == '__main__':
    main()
