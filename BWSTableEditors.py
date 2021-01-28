from BWSDefinitions import *


def to_five_bit_signed(value):
    if value >= 0:
        return value & 0xF
    else:
        return (value + 0x10) & 0x1F


def to_six_bit_signed(value):
    if value >= 0:
        return value & 0x1F
    else:
        return (value + 0x30) & 0x3F


def to_eight_bit_signed(value):
    if value >= 0:
        return value & 0x7F
    else:
        return (value + 0x80) & 0xFF


def write_x_bits(buffer, offset, x_bits, bit_offset, value):
    value &= ((1 << x_bits) - 1)
    buffer[offset] = (buffer[offset] & (0xFF - (((1 << x_bits) - 1) << bit_offset) & 0xFF)) + ((value << bit_offset) & 0xFF)
    if bit_offset + x_bits > 8:
        buffer[offset + 1] = (buffer[offset + 1] & (0xFF - (((1 << x_bits) - 1) >> (8 - bit_offset)))) + (
                value >> (8 - bit_offset))


def read_x_bits(buffer, offset, x_bits, bit_offset):
    value = ((0xFF << bit_offset) & 0xFF & buffer[offset]) >> bit_offset
    if bit_offset + x_bits > 8:
        value += (buffer[offset + 1] & (0xFF >> (8 - bit_offset))) << (8 - bit_offset)
    return value


def modify_x_bits(buffer, offset, x_bits, bit_offset, value):
    write_x_bits(buffer, offset, x_bits, bit_offset, read_x_bits(buffer, offset, x_bits, bit_offset) + value)


def set_base(buffer, unit, stat, value):
    offsets = UnitOffset + UnitToOffset[unit], UnitOffset2 + UnitToOffset[unit]
    for offset in offsets:
        if stat == "level" or stat == "lv":
            write_x_bits(buffer, offset + 20, 6, 0, value)
        elif stat == "hp":
            write_x_bits(buffer, offset + 22, 7, 4, value)
        elif stat == "strength" or stat == "str":
            write_x_bits(buffer, offset + 23, 5, 3, to_five_bit_signed(value))
        elif stat == "speed" or stat == "spe" or stat == "spd":
            write_x_bits(buffer, offset + 24, 5, 0, to_five_bit_signed(value))
        elif stat == "luck" or stat == "luk":
            write_x_bits(buffer, offset + 24, 5, 5, to_five_bit_signed(value))
        elif stat == "defense" or stat == "def":
            write_x_bits(buffer, offset + 25, 5, 2, to_five_bit_signed(value))
        elif stat == "mind" or stat == "magic" or stat == "mag":
            write_x_bits(buffer, offset + 25, 5, 7, to_five_bit_signed(value))
        elif stat == "knife":
            write_x_bits(buffer, offset + 36, 10, 0, value * 10)
        elif stat == "sword":
            write_x_bits(buffer, offset + 37, 10, 2, value * 10)
        elif stat == "spear" or stat == "lance":
            write_x_bits(buffer, offset + 38, 10, 4, value * 10)
        elif stat == "axe":
            write_x_bits(buffer, offset + 40, 10, 0, value * 10)
        elif stat == "bow":
            write_x_bits(buffer, offset + 41, 10, 2, value * 10)
        elif stat == "crossbow":
            write_x_bits(buffer, offset + 42, 10, 4, value * 10)
        elif stat == "fire":
            write_x_bits(buffer, offset + 44, 10, 0, value * 10)
        elif stat == "thunder":
            write_x_bits(buffer, offset + 45, 10, 2, value * 10)
        elif stat == "wind":
            write_x_bits(buffer, offset + 46, 10, 4, value * 10)
        elif stat == "holy" or stat == "light":
            write_x_bits(buffer, offset + 48, 10, 0, value * 10)
        elif stat == "dark":
            write_x_bits(buffer, offset + 49, 10, 2, value * 10)
        elif stat == "sshield":
            write_x_bits(buffer, offset + 50, 10, 4, value * 10)
        elif stat == "mshield":
            write_x_bits(buffer, offset + 52, 10, 0, value * 10)
        elif stat == "lshield":
            write_x_bits(buffer, offset + 53, 10, 2, value * 10)
        elif stat == "mainhand" or stat == "weapon":
            write_x_bits(buffer, offset + 26, 4, 4, value)
        elif stat == "offhand" or stat == "shield" or stat == "accessory":
            write_x_bits(buffer, offset + 27, 4, 0, value)


def set_growth(buffer, unit, stat, value):
    offsets = GrowthOffset + (UnitToIndex[unit] - 1) * 32, GrowthOffset2 + (UnitToIndex[unit] - 1) * 32
    if stat == "bracket" and not value.isdigit():
        value = {"no": 1, "loose": 2, "strict": 3}[value]
    for offset in offsets:
        if stat == "hp":
            write_x_bits(buffer, offset, 7, 0, value)
        elif stat == "strength" or stat == "str":
            write_x_bits(buffer, offset, 7, 7, value)
        elif stat == "mind" or stat == "magic" or stat == "mag":
            write_x_bits(buffer, offset + 5, 7, 0, value)
        elif stat == "speed" or stat == "spe" or stat == "spd":
            write_x_bits(buffer, offset + 4, 7, 2, value)
        elif stat == "defense" or stat == "def":
            write_x_bits(buffer, offset + 1, 7, 6, value)
        elif stat == "knife":
            write_x_bits(buffer, offset + 8, 4, 0, value // 10)
        elif stat == "sword":
            write_x_bits(buffer, offset + 8, 4, 4, value // 10)
        elif stat == "spear" or stat == "lance":
            write_x_bits(buffer, offset + 9, 4, 0, value // 10)
        elif stat == "axe":
            write_x_bits(buffer, offset + 9, 4, 4, value // 10)
        elif stat == "bow":
            write_x_bits(buffer, offset + 10, 4, 0, value // 10)
        elif stat == "crossbow":
            write_x_bits(buffer, offset + 10, 4, 4, value // 10)
        elif stat == "fire":
            write_x_bits(buffer, offset + 11, 4, 0, value // 10)
        elif stat == "thunder":
            write_x_bits(buffer, offset + 11, 4, 4, value // 10)
        elif stat == "wind":
            write_x_bits(buffer, offset + 12, 4, 0, value // 10)
        elif stat == "holy" or stat == "light":
            write_x_bits(buffer, offset + 12, 4, 4, value // 10)
        elif stat == "dark":
            write_x_bits(buffer, offset + 13, 4, 0, value // 10)
        elif stat == "shield" or stat == "sshield" or stat == "mshield" or stat == "lshield":
            write_x_bits(buffer, offset + 13, 4, 4, value // 10)
        elif stat == "bracket":
            write_x_bits(buffer, offset + 2, 2, 5, value)


def set_skill(buffer, unit, skll_name, value):
    index = Skills.index(skll_name)
    offset = UnitOffset + UnitToOffset[unit]
    write_x_bits(buffer, offset + 56 + index // 8, 1, index & 0x7, value)
    offset = UnitOffset2 + UnitToOffset[unit]
    write_x_bits(buffer, offset + 56 + index // 8, 1, index & 0x7, value)


def set_item(buffer, unit, slot, item, durability, is_locked, is_dropped):
    offsets = UnitOffset + UnitToOffset[unit] + 0xBC + slot * 8, UnitOffset2 + UnitToOffset[unit] + 0xBC + slot * 8
    for offset in offsets:
        write_x_bits(buffer, offset, 16, 0, item)
        write_x_bits(buffer, offset + 2, 8, 4, durability)
        write_x_bits(buffer, offset + 4, 1, 3, int(is_locked))
        write_x_bits(buffer, offset + 3, 1, 8, int(is_dropped))


def set_bag_item(buffer, unit, slot, item, durability, is_locked, is_dropped):
    pass


def set_learned(buffer, unit, slot, skill, level):
    skill = Skills2.index(skill)
    offset = GrowthOffset + (UnitToIndex[unit] - 1) * 32
    write_x_bits(buffer, offset + 20 + slot, 8, 0, level)
    write_x_bits(buffer, offset + 26 + slot, 8, 0, skill)
    offset = GrowthOffset2 + (UnitToIndex[unit] - 1) * 32
    write_x_bits(buffer, offset + 20 + slot, 8, 0, level)
    write_x_bits(buffer, offset + 26 + slot, 8, 0, skill)


def set_support(buffer, unit, slot, source, amount):
    pass


def set_item_stat(buffer, item, stat, value):
    offsets = ItemOffset + (ItemToIndex[item] - 1) * 56, ItemOffset2 + (ItemToIndex[item] - 1) * 56
    for offset in offsets:
        if stat == "might":
            write_x_bits(buffer, offset, 6, 5, value)
        elif stat == "hex":
            write_x_bits(buffer, offset + 1, 4, 3, value)
        elif stat == "accuracy":
            write_x_bits(buffer, offset + 1, 7, 7, value)
        elif stat == "weight":
            write_x_bits(buffer, offset + 2, 5, 6, value)
        elif stat == "max_range":
            write_x_bits(buffer, offset + 3, 5, 3, value)
        elif stat == "min_range":
            write_x_bits(buffer, offset + 4, 4, 0, value)
        elif stat == "crit" or stat == "critical":
            write_x_bits(buffer, offset + 5, 7, 0, value)
        elif stat == "uses":
            write_x_bits(buffer, offset + 5, 7, 7, value)
        elif stat == "level":
            write_x_bits(buffer, offset + 6, 6, 6, value)
        elif stat == "price":
            write_x_bits(buffer, offset + 8, 16, 0, value)
        elif stat == "defense" or stat == "def":
            write_x_bits(buffer, offset + 12, 6, 0, to_six_bit_signed(value))
        elif stat == "speed" or stat == "spe" or stat == "spd":
            write_x_bits(buffer, offset + 13, 5, 3, to_five_bit_signed(value))
        elif stat == "avoid" or stat == "avo":
            write_x_bits(buffer, offset + 14, 8, 0, to_eight_bit_signed(value))
        elif stat == "hit":
            write_x_bits(buffer, offset + 15, 8, 0, to_eight_bit_signed(value))
        elif stat == "magic" or stat == "mind":
            write_x_bits(buffer, offset + 16, 5, 0, to_five_bit_signed(value))
        elif stat == "strength":
            write_x_bits(buffer, offset + 16, 5, 5, to_five_bit_signed(value))
        elif stat == "rounds":
            write_x_bits(buffer, offset + 17, 4, 2, value)
        elif stat == "fire_res":
            write_x_bits(buffer, offset + 17, 6, 6, to_six_bit_signed(value))
        elif stat == "thunder_res":
            write_x_bits(buffer, offset + 18, 6, 4, to_six_bit_signed(value))
        elif stat == "wind_res":
            write_x_bits(buffer, offset + 19, 6, 2, to_six_bit_signed(value))
        elif stat == "dark_res":
            write_x_bits(buffer, offset + 20, 6, 0, to_six_bit_signed(value))
        elif stat == "holy_res":
            write_x_bits(buffer, offset + 20, 6, 6, to_six_bit_signed(value))
        elif stat == "durability":
            write_x_bits(buffer, offset + 21, 3, 4, Durability.index(value))
        elif stat == "crit_avoid_penalty":
            write_x_bits(buffer, offset + 21, 8, 7, to_eight_bit_signed(value))


def set_item_effect(buffer, item, effect, value):
    eff_id = ItemEffects.index(effect)
    offset = ItemOffset + (ItemToIndex[item] - 1) * 56
    write_x_bits(buffer, offset + 28 + eff_id//8, 1, eff_id & 0x7, value)
    offset = ItemOffset2 + (ItemToIndex[item] - 1) * 56
    write_x_bits(buffer, offset + 28 + eff_id // 8, 1, eff_id & 0x7, value)


def set_item_effect_value(buffer, item, effect, value):
    offsets = ItemOffset + (ItemToIndex[item] - 1) * 56, ItemOffset2 + (ItemToIndex[item] - 1) * 56
    eff_id = ItemEffectRates.index(effect)
    for offset in offsets:
        if effect == 0:
            write_x_bits(buffer, offset + 26, 7, 0, 0)
            write_x_bits(buffer, offset + 27, 8, 0, 0)
            return
        write_x_bits(buffer, offset + 26, 7, 0, value)
        write_x_bits(buffer, offset + 27, 8, 0, eff_id + 100)


def set_class_base(buffer, cls, stat, value):
    offsets = ClassOffset + (ClassToIndex[cls] - 1) * 100, ClassOffset2 + (ClassToIndex[cls] - 1) * 100
    for offset in offsets:
        if stat == "hp":
            write_x_bits(buffer, offset, 5, 0, value)
        elif stat == "strength" or stat == "str":
            write_x_bits(buffer, offset, 5, 5, value)
        elif stat == "speed" or stat == "spe":
            write_x_bits(buffer, offset + 1, 5, 2, value)
        elif stat == "defense" or stat == "def":
            write_x_bits(buffer, offset + 2, 5, 0, value)
        elif stat == "magic" or stat == "mag" or stat == "mind":
            write_x_bits(buffer, offset + 2, 5, 5, value)
        elif stat == "move" or stat == "mov":
            write_x_bits(buffer, offset + 8, 4, 0, value)
        elif stat == "experience" or stat == "exp":
            write_x_bits(buffer, offset + 4, 7, 0, value)


def set_class_growth(buffer, cls, stat, value):
    offsets = ClassOffset + (ClassToIndex[cls] - 1) * 100, ClassOffset2 + (ClassToIndex[cls] - 1) * 100
    for offset in offsets:
        if stat == "hp":
            write_x_bits(buffer, offset + 24, 7, 0, value)
        elif stat == "strength" or stat == "str":
            write_x_bits(buffer, offset + 24, 7, 7, value)
        elif stat == "speed" or stat == "spe":
            write_x_bits(buffer, offset + 25, 7, 6, value)
        elif stat == "defense" or stat == "def":
            write_x_bits(buffer, offset + 26, 7, 5, value)
        elif stat == "magic" or stat == "mag" or stat == "mind":
            write_x_bits(buffer, offset + 28, 7, 0, value)


def set_class_caps(buffer, cls, stat, value):
    offsets = ClassOffset + (ClassToIndex[cls] - 1) * 100, ClassOffset2 + (ClassToIndex[cls] - 1) * 100
    for offset in offsets:
        if stat == "knife":
            write_x_bits(buffer, offset + 28, 6, 7, value)
        elif stat == "sword":
            write_x_bits(buffer, offset + 29, 6, 5, value)
        elif stat == "spear" or stat == "lance":
            write_x_bits(buffer, offset + 30, 6, 3, value)
        elif stat == "axe":
            write_x_bits(buffer, offset + 31, 6, 1, value)
        elif stat == "bow":
            write_x_bits(buffer, offset + 32, 6, 0, value)
        elif stat == "crossbow":
            write_x_bits(buffer, offset + 32, 6, 6, value)
        elif stat == "fire":
            write_x_bits(buffer, offset + 33, 6, 4, value)
        elif stat == "thunder":
            write_x_bits(buffer, offset + 34, 6, 2, value)
        elif stat == "wind":
            write_x_bits(buffer, offset + 35, 6, 0, value)
        elif stat == "holy" or stat == "light":
            write_x_bits(buffer, offset + 36, 6, 0, value)
        elif stat == "dark":
            write_x_bits(buffer, offset + 36, 6, 6, value)
        elif stat == "sshield":
            write_x_bits(buffer, offset + 37, 6, 4, value)
        elif stat == "mshield":
            write_x_bits(buffer, offset + 38, 6, 2, value)
        elif stat == "lshield":
            write_x_bits(buffer, offset + 39, 6, 0, value)


def set_class_attribute(buffer, cls, attribute, value):
    offsets = ClassOffset + (ClassToIndex[cls] - 1) * 100, ClassOffset2 + (ClassToIndex[cls] - 1) * 100
    value = MovementTypes.index(value)
    for offset in offsets:
        if attribute == "type":
            pass  # dunno
        elif attribute == "movement":
            write_x_bits(buffer, offset + 6, 4, 1, value)
        elif attribute == "mount":
            write_x_bits(buffer, offset + 3, 2, 4, value)


def set_class_skill(buffer, cls, stat, value):
    wid = Skills.index(stat)
    offset = ClassOffset + (ClassToIndex[cls] - 1) * 100
    write_x_bits(buffer, offset + 12 + wid//8, 1, wid & 0x7, value)
    offset = ClassOffset2 + (ClassToIndex[cls] - 1) * 100
    write_x_bits(buffer, offset + 12 + wid // 8, 1, wid & 0x7, value)
