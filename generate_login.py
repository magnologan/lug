#!/usr/bin/python
import os.path
import string
from unidecode import unidecode
from sys import exit
from sys import argv
import re

'''
    Create a combiantion of possible login names with with employee
    [+] :: Jonathan Dwight Jones :: ...
    will be generated:
        jonathan.dwight
        jonathan.jones

        OR

        jdwight
        jjones
'''

class Login(object):
    def __init__(self, filename=None, model='firstletter'):
        self.lines = self.openfile(filename)
        self.output = 'emails_linkedin.txt'
        self.model = model


    def openfile(self, filename):
        lines = list()
        if os.path.exists(filename):
            with open(filename, 'r') as fp:
                lines = [x.strip() for x in fp.read().splitlines()]
        return lines


    def combinations(self, names):
        first = names[0] if self.model == 'firstname' else names[0][0]
        if self.model == 'firstletter':
            first = '{}'.format(names[0][0])
        elif self.model == 'firstnamedot':
            first = '{}.'.format(names[0])
        elif self.model == 'firstname':
            first = '{}'.format(names[0])
        else:
            first = ''

        aux = list()
        for word in names[1:]:
            if len(word) < 3:
                continue
            aux.append('{}{}'.format(first,word))
        return aux


    def save(self, names):
        names = sorted(names)
        for n in names:
            print('{}'.format(n))

    def extract(self):
        allnames = set()
        for line in self.lines:
            m = re.search(r'\[\+\] :: (.*) :: .*', line)
            if m:
                words = m.group(1)
                words = unidecode(words).lower()
                exclude = set(string.punctuation)
                names = ''.join(ch for ch in words if ch not in exclude).split(' ')
                combis = self.combinations(names)
                if 'usuario.linkedin' in combis:
                    continue
                allnames.update(combis)
        self.save(allnames)


if __name__ == '__main__':
    if len(argv) < 2:
        print('Erro: Provide the result of extract.py.')
        print('Usage: {} [firstletter | firstname | firstnamedot] <list_of_names.txt>.'.format(argv[0]))
        exit(1)

    if len(argv) == 2:
        filename = argv[1]
        model = 'firstletterdot'
    else:
        filename = argv[2]
        model = argv[1]

    Login(filename=filename, model=model).extract()
