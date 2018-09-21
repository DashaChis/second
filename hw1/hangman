import random

hangmans = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''','''
  +---+
  |   |
  O   |
      |
      |
      |
=========''','''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''','''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''','''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''','''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''','''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']


def first_choice():
    print('выберите тему: страны(1), созвездия(2) или направления в искусстве(3)')
    a = input()
    if a == '1':
        return 'countries'
    if a == '2':
        return 'constellations'
    if a == '3':
        return 'art_movements'

def getword(a):
    with open(a + '.txt', encoding='UTF-8') as f:
        words = f.read()
        words = words.split()
        puzzle = random.choice(words)
    return puzzle

def hangman(draw, wronglet, correctlet, puzzle):
    print(draw[len(wronglet)])
    print()
    if 1 < len(wronglet) < 5:
        print('осталось', 6-len(wronglet), 'попытки')
    elif len(wronglet) == 5:
        print('последняя попытка!')
    else:
        print('осталось', 6-len(wronglet), 'попыток')
        
    none = '_'*len(puzzle)

    for i in range(len(puzzle)):
        if puzzle[i] in correctlet:
            none = none[:i] + puzzle[i] + none[i+1:]

    for letter in none:
        print(letter, end=' ')
    print()

def approve(twin):
    while True:
        alfabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        print('Введите букву:')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('буква ')
        elif guess in twin:
              print ('было уже, выберите другую букву!')
        elif guess not in alfabet:
              print('введите букву кириллицы')
        else:
              return guess

def main():
    wronglet = ''
    correctlet = ''
    puzzle = getword(first_choice())
    finish = False

    while True:
        hangman(hangmans, wronglet, correctlet, puzzle)
        abc = approve(wronglet + correctlet)
        if abc in puzzle:
            print('да, такая буква есть')
            correctlet = correctlet + abc
            foundall = True
            for i in range(len(puzzle)):
                if puzzle[i] not in correctlet:
                    foundall = False
                    break
            if foundall:
                print('Ура! Было загадано слово "' + puzzle + '"!')
                finish = True
        else:  
            wronglet = wronglet + abc
            if len(wronglet) == len(hangmans) - 1:
                hangman(hangmans, wronglet, correctlet, puzzle)
                print('Эх... Загаданное слово:"' + puzzle + '"')
                finish = True

        

if __name__ == '__main__':
    main()
    
