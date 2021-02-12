
import csv


Skills = [
    "locktouch", "canto", "overwatch", "watchful", "tripleshot", "counter", "shieldfaire", "mercy",
    "adept", "vantage", "vengeful", "spearbane", "provoke", "safezone", "guard", "astra",
    "arrowbane", "commander", "paragon", "fortune", "obfuscate", "steal", "silence", "hateful", "battlecry",
    "blessing", "sunder", "charisma", "acrobat", "evasion", "--", "--", "axeguard",
    "deadeye", "huntsman", "aim", "swimmer", "resistor", "search", "onetwo", "deathmatch",
    "horseswap", "throw", "parry", "prepared", "robust", "vulnerable", "focuschant", "ourbond",
    "horselover", "robbery", "despoil", "knockaway", "iaido", "pulverize", "mug2", "miracle",
    "armsthrift", "hide", "hurry", "lance", "blade", "--", "--", "cavalry", "celerity",
    "swordbane", "axebane", "limited", "convert", "expert", "magicbane", "mug", "versatile",
    "slowstart", "pitchfork", "pursuit", "doubleshot", "commander2", "return", "camouflage", "scotopic",
    "supporter", "climber", "windsweep", "desperation", "flourish", "slowstart2",  "robust2",
    "imbue", "critical", "protector", "debility", "maim", "--", "--"
]

Skills2 = [
    "locktouch", "canto", "overwatch", "watchful", "tripleshot", "counter", "shieldfaire", "mercy",
    "adept", "vantage", "vengeful", "spearbane", "provoke", "safezone", "guard", "astra",
    "arrowbane", "commander", "paragon", "fortune", "obfuscate", "steal", "silence", "hateful", "battlecry",
    "blessing", "sunder", "charisma", "acrobat", "evasion", "axeguard",
    "deadeye", "huntsman", "aim", "swimmer", "resistor", "search", "onetwo", "deathmatch",
    "horseswap", "throw", "parry", "prepared", "robust", "vulnerable", "focuschant", "ourbond",
    "horselover", "robbery", "despoil", "knockaway", "iaido", "pulverize", "mug2", "miracle",
    "armsthrift", "hide", "hurry", "lance", "blade", "cavalry", "celerity",
    "swordbane", "axebane", "limited", "convert", "expert", "magicbane", "mug", "versatile",
    "slowstart", "pitchfork", "pursuit", "doubleshot", "commander2", "return", "camouflage", "scotopic",
    "supporter", "climber", "windsweep", "desperation", "flourish", "slowstart2",  "robust2",
    "imbue", "critical", "protector", "debility", "maim"
]

ItemEffects = [
    "--", "female-locked", "x2", "x3", "x4", "--", "--", "--", "--", "--", "ignore-defense", "--",
    "ignore-shields", "ignore-armor-defense", "ignore-horse-defense", "--", "miracle", "renewal",
    "cripple-x2", "numerical-durability", "no-counter", "cant-move", "--", "--", "chance-def-up", "defend-adjacent",
    "gigas-knight-locked", "nosferatu", "damage-exp", "general-locked",
    "infantry-only", "--", "user-locked", "--", "unbreakable", "dunno-ballista-thing", "--", "--", "--",
    "??", "unobtainable-dagger", "unobtainable-arrow", "unobtainable-mace", "money", "--", "hide", "overwatch", "parry",
    "--", "--", "--", "--", "vritra-damage-reduction", "??", "--", "??", "cant-kill", "--",
    "add-level-to-damage", "scorpion-thing", "throwable", "--", "--", "to-broken-weapon", "horse", "famed-horse",
    "move+1", "--", "--", "paladin-locked", "star-icon", "--",
    "assassin-lock", "100%-against-bows", "--", "--", "--", "--", "--",
    "blackrider-locked", "apostle-locked", "horse-lover", "pascanion-backfire", "holy-vantage",
    "cant-attack-fliers", "--", "restore-uses", "--", "--", "--", "material", "--", "--", "--", "--", "--"
]

ItemEffectRates = [
    "half-damage", "--", "devil-reversal", "--", "steal-rate-plus", "thunder-damage", "fire-damage", "wind-damage",
    "sword-break", "--", "kill-horse", "break-shield", "--", "poison", "sleep", "--", "negate-dark", "negate-crit",
    "reflect-damage", "up-growth", "--", "cripple-rate", "--", "dark-damage", "holy-damage", "to-broken-weapon?",
    "block-fire-damage", "--", "block-thunder-damage", "--", "disarm-rate", "injure-rate", "--", "block-holy-damage"
]

Durability = ["s", "a", "b", "c", "d", "e", "f"]

WeaponTypes = ["knife", "sword", "blade", "mace", "spear", "lance", "fork", "axe", "bow", "crossbow", "ballista",
               "fire", "thunder", "wind", "holy", "dark", "holy_heal", "dark_heal", "sshield", "mshield", "lshield",
               "arrow", "bolt", "accessory", "consumable"]

WeaponTypes2 = ["knife", "sword", "blade", "mace", "spear", "lance", "fork", "axe", "bow", "crossbow", "ballista",
                "fire", "thunder", "wind", "holy", "dark", "holy1", "dark1", "--", "--",
                "sshield", "mshield", "lshield", "--"]

MountStatus = ["not_mounted", "mounted", "dismounted"]

UnitTypes = ["calvary", "infantry", "armor", "thief", "lt-infantry", "magic", "priest", "flier"]

MovementTypes = ["calvary", "lt-calvary", "flier", "knight", "armor", "infantry", "thief", "normal", "special", "snow",
                 "war-priest", "lt-infantry", "priest", "--"]


# first is japanese original, second is translation patch
UnitOffsets = (0x0890E9f0, 0x08DD7830), (0x0891A9f0, 0x08DE3830)
GrowthOffsets = (0x0CB4520, 0x08E907f4), (0x0CAAD20, 0x08EA7FF4)
ClassOffsets = (0x0CAE5CC, 0x08E8A8A0), (0x0CA4DCC, 0x08EA20A0)
ItemOffsets = (0x0CC0C04, 0x08E9CE08), (0x0CB7404, 0x08EB46D8)

UnitToIndex = {}
IndexToUnit = {}
UnitToOffset = {}
ClassToIndex = {}
IndexToClass = {}
ItemToIndex = {}
IndexToItem = {}

with open('data/characters.csv', newline='') as file:
    reader = csv.reader(file)
    for chara, index, offset in reader:
        index = eval(index)
        UnitToIndex[chara.lower()] = index
        IndexToUnit[index] = chara.lower()
        UnitToOffset[chara.lower()] = eval(offset)

with open('data/classes.csv', newline='') as file:
    reader = csv.reader(file)
    for cl, index in reader:
        index = eval(index)
        ClassToIndex[cl.lower()] = index
        IndexToClass[index] = cl.lower()

with open('data/items.csv', newline='') as file:
    reader = csv.reader(file)
    for item, index in reader:
        index = eval(index)
        ItemToIndex[item.lower()] = index
        IndexToItem[index] = item.lower()

