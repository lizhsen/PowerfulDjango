# coding = utf-8
import unittest
import random
# mylist = ['c', 'a', 't', 'd', 'o', 'g', 'r', 'a', 'b', 'b', 'i', 't']
# d = set()
# for i in range(len(mylist)):
#     d.add(mylist[i])
# print d


def test_sigle_letter():
    wordlist = ['cat','dog','rabbit']
    letterlist = []
    for aword in wordlist:
        for aletter in aword:
            if aletter in letterlist:
                pass
            else:
                letterlist.append(aletter)
    print(letterlist)


def make_random():
    str = 'abcdefghijklmnopqrstuvwxy z'
    word = ''
    for j in range(23):
        i = random.randint(0,26)
        word += str[i]
    return word


def compare_word():
    word = make_random()
    i = 1
    while i <= 10000000000:
        if "methinks it is a wwasel" == word:
            print i
        else:
            word = make_random()
        i += 1
    print i


# test_sigle()
#make_random()


compare_word()




