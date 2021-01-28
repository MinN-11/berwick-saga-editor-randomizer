import sys
from BWSTableEditors import *


def try_eval(str):
    try:
        return eval(str)
    except:
        return str


def help():
    print("How to run this program:")
    print("python3 bwseditor.py Data3.dat Output.dat your_script")
    print("How to write the script:")
    print("set          unit_name/class_name base/growth stat_name #stat_value")
    print("                 If a value is like +5 or -4, modify the original value instead")
    print("set/unset    unit_name/class_name skill_name")
    print("set/unset    unit_name learned skill_name #level")
    print("set/unset    unit bracket tight/loose/no")
    print("set/unset    unit item #slot item_name max/#uses [lock] [drop]")
    print("                 WARNING: max only works on weapons with colored durability, aka 101.")
    print("                 [lock] is mercenary lock, [drop] is drop item.")
    # print("set          unit bag  #slot item_name max/#uses  [lock] [drop]")
    # print("                 WARNING: This does not allocate new space, can only modify existing items.")
    print("set          item stat stat_name #value")
    print("set          item effect effect_flag_name")
    print("set          item effect effect_name #value")
    print("")


def list_stuff():
    if len(sys.argv) < 3:
        return
    if sys.argv[2] == "unit":
        for i in UnitToIndex:
            print(i, end=", ")
    elif sys.argv[2] == "item":
        for i in ItemToIndex:
            print(i, end=", ")
    elif sys.argv[2] == "class":
        for i in ClassToIndex:
            print(i, end=", ")
    print()


def main():
    if len(sys.argv) < 2:
        pass
    elif sys.argv[1] == "help":
        help()
    elif sys.argv[1] == "list":
        list_stuff()
    elif len(sys.argv) < 4:
        print("python3 init.py DATA3.DAT OUTPUT YOUR_SCRIPT")
    if len(sys.argv) < 4:
        quit()
    _, data, output, script = sys.argv[:4]
    with open(data, "rb") as data_file:
        buffer = bytearray(data_file.read())
    with open(script, "r") as script_file:
        for line in script_file:
            try:
                commands = line.strip().lower().split(" ")
                if len(commands) <= 1:
                    continue
                if commands[0].startswith("//"):
                    continue
                target = commands[1]
                if target in UnitToIndex:
                    if commands[0] == "set":
                        if commands[2] == "base":
                            set_base(buffer, target, commands[3], try_eval(commands[4]))
                        elif commands[2] == "growth":
                            set_growth(buffer, target, commands[3], try_eval(commands[4]))
                        elif commands[2] == "skill":
                            set_skill(buffer, target, commands[3], 1)
                        elif commands[2] == "item":
                            if commands[5] == "max":
                                commands[5] = "101"
                            set_item(buffer, target, try_eval(commands[3]), ItemToIndex[commands[4]], try_eval(commands[5]),
                                     "lock" in commands, "drop" in commands)
                        elif commands[2] == "bag":
                            set_bag_item(buffer, target, try_eval(commands[3]), ItemToIndex[commands[4]], try_eval(commands[5]),
                                         "lock" in commands, "drop" in commands)
                        elif commands[2] == "support":
                            set_support(buffer, target, try_eval(commands[3]), commands[4], try_eval(commands[5]))
                        elif commands[2] == "bracket":
                            set_growth(buffer, target, "bracket", commands[3])
                        elif commands[2] == "learned":
                            set_learned(buffer, target, try_eval(commands[3]), commands[4], try_eval(commands[5]))
                    elif commands[0] == "unset":
                        if commands[2] == "skill":
                            set_skill(buffer, target, commands[3], 0)
                        elif commands[2] == "item":
                            set_item(buffer, target, try_eval(commands[3]), 0, 0, False, False)
                        elif commands[2] == "bag":
                            set_bag_item(buffer, target, try_eval(commands[3]), 0, 0, False, False)
                        elif commands[2] == "learned":
                            set_learned(buffer, target, try_eval(commands[3]), 255, 0)
                elif target in ClassToIndex:
                    if commands[0] == "set":
                        if commands[2] == "base":
                            set_class_base(buffer, target, commands[3], try_eval(commands[4]))
                        elif commands[2] == "growth":
                            set_class_growth(buffer, target, commands[3], try_eval(commands[4]))
                        elif commands[2] == "skill":
                            set_class_skill(buffer, target, commands[3], 1)
                        elif commands[2] == "attribute":
                            set_class_attribute(buffer, target, commands[3], commands[4])
                    elif commands[0] == "unset":
                        if commands[2] == "skill":
                            set_class_skill(buffer, target, commands[3], 0)
                elif target in ItemToIndex:
                    if commands[0] == "set":
                        if commands[2] == "stat":
                            set_item_stat(buffer, target, commands[3], try_eval(commands[4]))
                        elif commands[2] == "effect":
                            if commands[3] in ItemEffects:
                                set_item_effect(buffer, target, commands[3], 1)
                            else:
                                set_item_effect_value(buffer, target, commands[3], try_eval(commands[4]))
                    elif commands[0] == "unset":
                        if commands[2] == "effect":
                            if commands[3] in ItemEffects:
                                set_item_effect(buffer, target, commands[3], 0)
                            else:
                                set_item_effect_value(buffer, target, 0, 0)
            except IndexError:
                print("Error parsing line {}".format(line))

    with open(output, "wb") as output_file:
        output_file.write(buffer)


if __name__ == '__main__':
    main()
