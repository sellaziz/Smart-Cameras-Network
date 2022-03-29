"""
Generate a csv file that gives you random scenes for the acquisition of your dataset depending on the input dictionary
"""
import random
from math import *
import csv

#classes = [0: nbr_of_mugs, 1:nbre_of_shoes, 2:nbre_of_mice, 3:nbr_of_books, 4:nbr_of_wallet, 5:nbr_of_keyboards, 6:nbr_of_pencilcase]
#positions = nbre_of positions
dic_class = {0: "mug", 1: "shoe", 2: "mouse", 3: "book", 4: "wallet", 5: "keyboard", 6: "pencilcase"}

def randomizer(positions, classes):
    f = open(r"C:\Users\heyzi\OneDrive\Documents\imta\smart_cam\room.txt","w")
    f.write("class object_nbr position class object_nbr position class object_nbr position\n")
    for i in range(500):
        nbr_of_object = math.log2(random.randint(1,8)) #50% 1 object 37.5% 2 objets 12.5% 3 objets
        if nbr_of_object <= 2:
            nbr_of_object = 1
        nbr_of_object = math.floor(nbr_of_object)
        for j in range(nbr_of_object):
             #print(j)
            which_class =  random.randint(0,6)
            which_object = random.randint(1,classes[which_class]) - 1
            which_position = random.randint(1,positions) - 1
            which_yaw = random.randint(-3,4)*45
            which_pitch = random.randint(0,2)*90
            f.write(dic_class[which_class] + " " + str(which_object) + " " + str(which_position) + " " + str(which_yaw) + " " + str(which_pitch) + " ")
        f.write("\n")
    f.close()


def randomizer2(positions, classes, nbr_of_shot):
    f = open(r"C:\Users\heyzi\OneDrive\Documents\imta\smart_cam\room.txt","w")
    f.write("class object_nbr position yaw pitch class object_nbr position yaw pitch class object_nbr position yaw pitch\n")

    # 50% 1 objet 30% 2 objets 20% 3 objets
    total_object = int(nbr_of_shot * 1.7)   # 50% + 2*30% + 3*20% = 170%
    total_each_class = 7*[floor(total_object/7)]

    plannification = []

    for i in range((nbr_of_shot*20)//100): #3 images

        row = []

        for j in range(3):

            which_class =  random.randint(0,6)        #on choisit une classe au hasard
            while total_each_class[which_class] == 0: #suffisamment d'objets de cette classe ont été utilisés
                print('plus de %i',which_class)
                which_class =  random.randint(0,6)    #on rechoisit
            total_each_class[which_class] -= 1        #on décrémente le nombre d'objet à utiliser de cette classe

            which_object = random.randint(1,classes[which_class]) - 1
            row.append([which_class, which_object])

        row.sort()
        plannification.append(row)

    for i in range((nbr_of_shot*30)//100): #2 images

        row = []

        for j in range(2):

            which_class =  random.randint(0,6)        #on choisit une classe au hasard
            while total_each_class[which_class] == 0: #suffisamment d'objets de cette classe ont été utilisés
                print('plus de %i',which_class)
                which_class =  random.randint(0,6)    #on rechoisit
            total_each_class[which_class] -= 1        #on décrémente le nombre d'objet à utiliser de cette classe

            which_object = random.randint(1,classes[which_class]) - 1
            row.append([which_class, which_object])

        row.sort()
        plannification.append(row)

    for i in range(7): #1 image

        for j in range(total_each_class[i]):

            row = []

            which_object = random.randint(1,classes[i]) - 1
            row.append([i, which_object])

            plannification.append(row)

    plannification.sort()

    for i in range(len(plannification)):
        #print(plannification[i])
        for j in range(len(plannification[i])):

            which_position = random.randint(1,positions) - 1
            which_yaw = random.randint(-3,4)*45
            which_pitch = random.randint(0,2)*90
            if plannification[i][j][0] == 5 and which_pitch == 90: #keyboard cannot be put vertically
                which_pitch = 0

            f.write(dic_class[plannification[i][j][0]] + " " + str(plannification[i][j][1]) + " " + str(which_position) + " " + str(which_yaw) + " " + str(which_pitch) + " ")
        f.write("\n")
    f.close()
