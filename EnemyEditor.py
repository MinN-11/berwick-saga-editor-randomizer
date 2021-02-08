
import random
from BWSDefinitions import *
from RandomizerDefinitions import *

Stats = [
     "hp", "strength", "speed", "defense", "magic"
]


def WriteEditor(file, value):
    with open(file, "w") as file:
        for cl in EnemyClasses:
            for stat in Stats:
                n = value
                if stat == "magic" and cl in ArmoredEnemies:
                    n = 0
                elif stat == "magic" and cl not in MagicalEnemies:
                    n = 1
                if stat == "hp":
                    n += 2
                elif stat == "defense" and cl not in ArmoredEnemies:
                    n //= 2
                file.write("set {} base {} +{}\n".format(cl, stat, n))


def SkillEditor(file, value):
    with open(file, "w") as file:
        for cl in EnemyClasses:
            file.write("set {} skill {}\n".format(cl, value))


def LunaticPlusEditor(file):
    with open(file, "w") as file:
        lunaticPlusSkills = ["pursuit", "vantage", "counter", "adept", "desperation"]
        lunaticPlusSkills2 = ["swordbane", "spearbane", "axebane", "arrowbane", "magicbane"]
        lunaticPlusSkills2_1 = ["swordbane", "spearbane", "axebane", "arrowbane", "shieldfaire"]
        for cl in EnemyClasses:
            s1 = random.choice(lunaticPlusSkills)
            s2 = random.choice(lunaticPlusSkills2 if cl not in ArmoredEnemies else lunaticPlusSkills2_1)
            file.write("set {} skill {}\n".format(cl, s1))
            file.write("set {} skill {}\n".format(cl, s2))


LunaticPlusEditor("bws_lunatic_plus.txt")