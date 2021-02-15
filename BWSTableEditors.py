from BWSDefinitions import *


LanguageUsed = 1  # 0 is japanese, 1 is translation patch, globals are bad I know


def SetLanguageUsed(v):
    global LanguageUsed
    LanguageUsed = v


class UnknownAttributeError(Exception):
    pass


class UnknownCommandError(Exception):
    pass


class UnknownItemError(Exception):
    pass


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
    value = ((0xFF >> (8 - x_bits) << bit_offset) & 0xFF & buffer[offset]) >> bit_offset
    if bit_offset + x_bits > 8:
        value += (buffer[offset + 1] & ((1 << bit_offset + x_bits - 8) - 1)) << (8 - bit_offset)
    return value


def modify_x_bits(buffer, offset, x_bits, bit_offset, value, modifier, ma=65535, mi=0):
    if modifier == 1:
        value = read_x_bits(buffer, offset, x_bits, bit_offset) + value
    elif modifier == -1:
        value = read_x_bits(buffer, offset, x_bits, bit_offset) - value
    elif modifier == 2:
        value = int(read_x_bits(buffer, offset, x_bits, bit_offset) * value)
    value = 0 if value < 0 else (1 << x_bits) - 1 if value >= 1 << x_bits else value
    value = max(mi, min(ma, value))
    write_x_bits(buffer, offset, x_bits, bit_offset, value)


def set_base(buffer, unit, stat, value):
    value, modifier = value
    offsets = UnitOffsets[LanguageUsed][0] + UnitToOffset[unit], UnitOffsets[LanguageUsed][1] + UnitToOffset[unit]
    for offset in offsets:
        if stat == "level" or stat == "lv" or stat == "rank":
            modify_x_bits(buffer, offset + 20, 6, 0, value, modifier)
        elif stat == "hp":
            modify_x_bits(buffer, offset + 22, 7, 4, value, modifier)
        elif stat == "strength" or stat == "str":
            modify_x_bits(buffer, offset + 23, 5, 3, to_five_bit_signed(value), modifier)
        elif stat == "speed" or stat == "spe" or stat == "spd":
            modify_x_bits(buffer, offset + 24, 5, 0, to_five_bit_signed(value), modifier)
        elif stat == "luck" or stat == "luk":
            modify_x_bits(buffer, offset + 24, 5, 5, to_five_bit_signed(value), modifier)
        elif stat == "defense" or stat == "def":
            modify_x_bits(buffer, offset + 25, 5, 2, to_five_bit_signed(value), modifier)
        elif stat == "mind" or stat == "magic" or stat == "mag":
            modify_x_bits(buffer, offset + 25, 5, 7, to_five_bit_signed(value), modifier)
        elif stat == "knife":
            modify_x_bits(buffer, offset + 36, 10, 0, value * 10, modifier)
        elif stat == "sword":
            modify_x_bits(buffer, offset + 37, 10, 2, value * 10, modifier)
        elif stat == "spear" or stat == "lance":
            modify_x_bits(buffer, offset + 38, 10, 4, value * 10, modifier)
        elif stat == "axe":
            modify_x_bits(buffer, offset + 40, 10, 0, value * 10, modifier)
        elif stat == "bow":
            modify_x_bits(buffer, offset + 41, 10, 2, value * 10, modifier)
        elif stat == "crossbow":
            modify_x_bits(buffer, offset + 42, 10, 4, value * 10, modifier)
        elif stat == "fire":
            modify_x_bits(buffer, offset + 44, 10, 0, value * 10, modifier)
        elif stat == "thunder":
            modify_x_bits(buffer, offset + 45, 10, 2, value * 10, modifier)
        elif stat == "wind":
            modify_x_bits(buffer, offset + 46, 10, 4, value * 10, modifier)
        elif stat == "holy" or stat == "light":
            modify_x_bits(buffer, offset + 48, 10, 0, value * 10, modifier)
        elif stat == "dark":
            modify_x_bits(buffer, offset + 49, 10, 2, value * 10, modifier)
        elif stat == "sshield":
            modify_x_bits(buffer, offset + 50, 10, 4, value * 10, modifier)
        elif stat == "mshield":
            modify_x_bits(buffer, offset + 52, 10, 0, value * 10, modifier)
        elif stat == "lshield":
            modify_x_bits(buffer, offset + 53, 10, 2, value * 10, modifier)
        elif stat == "offhand":
            modify_x_bits(buffer, offset + 26, 4, 4, value + 1, modifier)  # 0 is unequipped
        elif stat == "mainhand":
            modify_x_bits(buffer, offset + 27, 4, 0, value + 1, modifier)  # 0 is unequipped
        else:
            raise UnknownAttributeError


def set_growth(buffer, unit, stat, value):
    value, modifier = value
    offsets = GrowthOffsets[LanguageUsed][0] + (UnitToIndex[unit] - 1) * 32, GrowthOffsets[LanguageUsed][1] + (UnitToIndex[unit] - 1) * 32
    if stat == "bracket" and not value.isdigit():
        value = {"no": 1, "loose": 2, "tight": 3}[value]
    for offset in offsets:
        if stat == "hp":
            modify_x_bits(buffer, offset, 7, 0, value, modifier)
        elif stat == "strength" or stat == "str":
            modify_x_bits(buffer, offset, 7, 7, value, modifier)
        elif stat == "mind" or stat == "magic" or stat == "mag":
            modify_x_bits(buffer, offset + 5, 7, 0, value, modifier)
        elif stat == "speed" or stat == "spe" or stat == "spd":
            modify_x_bits(buffer, offset + 4, 7, 2, value, modifier)
        elif stat == "defense" or stat == "def":
            modify_x_bits(buffer, offset + 1, 7, 6, value, modifier)
        elif stat == "knife":
            modify_x_bits(buffer, offset + 8, 4, 0, value // 10, modifier)
        elif stat == "sword":
            modify_x_bits(buffer, offset + 8, 4, 4, value // 10, modifier)
        elif stat == "spear" or stat == "lance":
            modify_x_bits(buffer, offset + 9, 4, 0, value // 10, modifier)
        elif stat == "axe":
            modify_x_bits(buffer, offset + 9, 4, 4, value // 10, modifier)
        elif stat == "bow":
            modify_x_bits(buffer, offset + 10, 4, 0, value // 10, modifier)
        elif stat == "crossbow":
            modify_x_bits(buffer, offset + 10, 4, 4, value // 10, modifier)
        elif stat == "fire":
            modify_x_bits(buffer, offset + 11, 4, 0, value // 10, modifier)
        elif stat == "thunder":
            modify_x_bits(buffer, offset + 11, 4, 4, value // 10, modifier)
        elif stat == "wind":
            modify_x_bits(buffer, offset + 12, 4, 0, value // 10, modifier)
        elif stat == "holy" or stat == "light":
            modify_x_bits(buffer, offset + 12, 4, 4, value // 10, modifier)
        elif stat == "dark":
            modify_x_bits(buffer, offset + 13, 4, 0, value // 10, modifier)
        elif stat == "shield" or stat == "sshield" or stat == "mshield" or stat == "lshield":
            modify_x_bits(buffer, offset + 13, 4, 4, value // 10, modifier)
        elif stat == "bracket":
            write_x_bits(buffer, offset + 2, 2, 5, value)
        else:
            raise UnknownAttributeError


def set_skill(buffer, unit, skll_name, value):
    index = Skills.index(skll_name)
    offset = UnitOffsets[LanguageUsed][0] + UnitToOffset[unit]
    write_x_bits(buffer, offset + 56 + index // 8, 1, index & 0x7, value)
    offset = UnitOffsets[LanguageUsed][1] + UnitToOffset[unit]
    write_x_bits(buffer, offset + 56 + index // 8, 1, index & 0x7, value)


def set_item(buffer, unit, slot, item, durability, is_locked, is_dropped):
    slot, _ = slot
    durability, _ = durability
    offsets = UnitOffsets[LanguageUsed][0] + UnitToOffset[unit] + 0xBC + slot * 8, UnitOffsets[LanguageUsed][1] + UnitToOffset[unit] + 0xBC + slot * 8
    for offset in offsets:
        write_x_bits(buffer, offset, 16, 0, item)
        write_x_bits(buffer, offset + 2, 8, 4, durability)
        write_x_bits(buffer, offset + 4, 1, 2, int(is_locked))
        write_x_bits(buffer, offset + 3, 1, 7, int(is_dropped))


def set_bag_item(buffer, unit, slot, item, durability, is_locked, is_dropped):
    pass
    # TODO: implement this


def set_learned(buffer, unit, slot, skill, level):
    slot, _ = slot
    level, modifier = level
    if isinstance(skill, str):
        skill = Skills2.index(skill)
    offset = GrowthOffsets[LanguageUsed][0] + (UnitToIndex[unit] - 1) * 32
    modify_x_bits(buffer, offset + 20 + slot, 8, 0, level, modifier)
    write_x_bits(buffer, offset + 26 + slot, 8, 0, skill)
    offset = GrowthOffsets[LanguageUsed][1] + (UnitToIndex[unit] - 1) * 32
    modify_x_bits(buffer, offset + 20 + slot, 8, 0, level, modifier)
    write_x_bits(buffer, offset + 26 + slot, 8, 0, skill)


def set_support(buffer, unit, slot, source, amount):
    pass


def set_item_stat(buffer, item, stat, value):
    value, modifier = value
    offsets = ItemOffsets[LanguageUsed][0] + (ItemToIndex[item] - 1) * 56, ItemOffsets[LanguageUsed][1] + (ItemToIndex[item] - 1) * 56
    for offset in offsets:
        if stat == "might":
            modify_x_bits(buffer, offset, 6, 5, value, modifier)
        elif stat == "hex":
            modify_x_bits(buffer, offset + 1, 4, 3, value, modifier)
        elif stat == "accuracy":
            modify_x_bits(buffer, offset + 1, 7, 7, value, modifier)
        elif stat == "weight":
            modify_x_bits(buffer, offset + 2, 5, 6, value, modifier)
        elif stat == "max_range" or stat == "max-range":
            modify_x_bits(buffer, offset + 3, 5, 3, value, modifier)
        elif stat == "min_range" or stat == "min-range":
            modify_x_bits(buffer, offset + 4, 4, 0, value, modifier)
        elif stat == "crit" or stat == "critical":
            modify_x_bits(buffer, offset + 5, 7, 0, value, modifier)
        elif stat == "uses":
            modify_x_bits(buffer, offset + 5, 7, 7, value, modifier)
        elif stat == "level":
            modify_x_bits(buffer, offset + 6, 6, 6, value, modifier)
        elif stat == "price" or stat == "cost":
            modify_x_bits(buffer, offset + 8, 16, 0, value, modifier, mi=100)  # for the randomizer
        elif stat == "defense" or stat == "def":
            modify_x_bits(buffer, offset + 12, 6, 0, to_six_bit_signed(value), modifier)
        elif stat == "speed" or stat == "spe" or stat == "spd":
            modify_x_bits(buffer, offset + 13, 5, 3, to_five_bit_signed(value), modifier)
        elif stat == "avoid" or stat == "avo":
            modify_x_bits(buffer, offset + 14, 8, 0, to_eight_bit_signed(value), modifier)
        elif stat == "hit":
            modify_x_bits(buffer, offset + 15, 8, 0, to_eight_bit_signed(value), modifier)
        elif stat == "magic" or stat == "mind":
            modify_x_bits(buffer, offset + 16, 5, 0, to_five_bit_signed(value), modifier)
        elif stat == "strength":
            modify_x_bits(buffer, offset + 16, 5, 5, to_five_bit_signed(value), modifier)
        elif stat == "rounds":
            modify_x_bits(buffer, offset + 17, 4, 2, value, modifier)
        elif stat == "fire_res":
            modify_x_bits(buffer, offset + 17, 6, 6, to_six_bit_signed(value), modifier)
        elif stat == "thunder_res":
            modify_x_bits(buffer, offset + 18, 6, 4, to_six_bit_signed(value), modifier)
        elif stat == "wind_res":
            modify_x_bits(buffer, offset + 19, 6, 2, to_six_bit_signed(value), modifier)
        elif stat == "dark_res":
            modify_x_bits(buffer, offset + 20, 6, 0, to_six_bit_signed(value), modifier)
        elif stat == "holy_res":
            modify_x_bits(buffer, offset + 20, 6, 6, to_six_bit_signed(value), modifier)
        elif stat == "durability":
            if isinstance(value, str):
                value = Durability.index(value)
            modify_x_bits(buffer, offset + 21, 3, 4, value, -modifier, ma=6)
        elif stat == "crit_avoid_penalty":
            modify_x_bits(buffer, offset + 21, 8, 7, to_eight_bit_signed(value), modifier)
        else:
            raise UnknownAttributeError


def set_item_effect(buffer, item, effect, value):
    eff_id = ItemEffects.index(effect)
    offset = ItemOffsets[LanguageUsed][0] + (ItemToIndex[item] - 1) * 56
    write_x_bits(buffer, offset + 28 + eff_id//8, 1, eff_id & 0x7, value)
    offset = ItemOffsets[LanguageUsed][1] + (ItemToIndex[item] - 1) * 56
    write_x_bits(buffer, offset + 28 + eff_id // 8, 1, eff_id & 0x7, value)


def set_item_effect_value(buffer, item, effect, value):
    value, modifier = value
    offsets = ItemOffsets[LanguageUsed][0] + (ItemToIndex[item] - 1) * 56, ItemOffsets[LanguageUsed][1] + (ItemToIndex[item] - 1) * 56
    eff_id = ItemEffectRates.index(effect)
    for offset in offsets:
        if effect == 0:
            write_x_bits(buffer, offset + 26, 7, 0, 0)
            write_x_bits(buffer, offset + 27, 8, 0, 0)
            return
        modify_x_bits(buffer, offset + 26, 7, 0, value, modifier)
        write_x_bits(buffer, offset + 27, 8, 0, eff_id + 100)


def set_class_base(buffer, cls, stat, value):
    value, modifier = value
    offsets = ClassOffsets[LanguageUsed][0] + (ClassToIndex[cls] - 1) * 100, ClassOffsets[LanguageUsed][1] + (ClassToIndex[cls] - 1) * 100
    for offset in offsets:
        if stat == "hp":
            modify_x_bits(buffer, offset, 5, 0, value, modifier)
        elif stat == "strength" or stat == "str":
            modify_x_bits(buffer, offset, 5, 5, value, modifier)
        elif stat == "speed" or stat == "spe":
            modify_x_bits(buffer, offset + 1, 5, 2, value, modifier)
        elif stat == "defense" or stat == "def":
            modify_x_bits(buffer, offset + 2, 5, 0, value, modifier)
        elif stat == "magic" or stat == "mag" or stat == "mind":
            modify_x_bits(buffer, offset + 2, 5, 5, value, modifier)
        elif stat == "move" or stat == "mov":
            modify_x_bits(buffer, offset + 8, 4, 0, value, modifier)
        elif stat == "experience" or stat == "exp":
            modify_x_bits(buffer, offset + 4, 7, 0, value, modifier)
        else:
            raise UnknownAttributeError


def set_class_growth(buffer, cls, stat, value):
    value, modifier = value
    offsets = ClassOffsets[LanguageUsed][0] + (ClassToIndex[cls] - 1) * 100, ClassOffsets[LanguageUsed][1] + (ClassToIndex[cls] - 1) * 100
    for offset in offsets:
        if stat == "hp":
            modify_x_bits(buffer, offset + 24, 7, 0, value, modifier)
        elif stat == "strength" or stat == "str":
            modify_x_bits(buffer, offset + 24, 7, 7, value, modifier)
        elif stat == "speed" or stat == "spe":
            modify_x_bits(buffer, offset + 25, 7, 6, value, modifier)
        elif stat == "defense" or stat == "def":
            modify_x_bits(buffer, offset + 26, 7, 5, value, modifier)
        elif stat == "magic" or stat == "mag" or stat == "mind":
            modify_x_bits(buffer, offset + 28, 7, 0, value, modifier)


def set_class_caps(buffer, cls, stat, value):
    value, modifier = value
    offsets = ClassOffsets[LanguageUsed][0] + (ClassToIndex[cls] - 1) * 100, ClassOffsets[LanguageUsed][1] + (ClassToIndex[cls] - 1) * 100
    for offset in offsets:
        if stat == "knife":
            modify_x_bits(buffer, offset + 28, 6, 7, value, modifier)
        elif stat == "sword":
            modify_x_bits(buffer, offset + 29, 6, 5, value, modifier)
        elif stat == "spear" or stat == "lance":
            modify_x_bits(buffer, offset + 30, 6, 3, value, modifier)
        elif stat == "axe":
            modify_x_bits(buffer, offset + 31, 6, 1, value, modifier)
        elif stat == "bow":
            modify_x_bits(buffer, offset + 32, 6, 0, value, modifier)
        elif stat == "crossbow":
            modify_x_bits(buffer, offset + 32, 6, 6, value, modifier)
        elif stat == "fire":
            modify_x_bits(buffer, offset + 33, 6, 4, value, modifier)
        elif stat == "thunder":
            modify_x_bits(buffer, offset + 34, 6, 2, value, modifier)
        elif stat == "wind":
            modify_x_bits(buffer, offset + 35, 6, 0, value, modifier)
        elif stat == "holy" or stat == "light":
            modify_x_bits(buffer, offset + 36, 6, 0, value, modifier)
        elif stat == "dark":
            modify_x_bits(buffer, offset + 36, 6, 6, value, modifier)
        elif stat == "sshield":
            modify_x_bits(buffer, offset + 37, 6, 4, value, modifier)
        elif stat == "mshield":
            modify_x_bits(buffer, offset + 38, 6, 2, value, modifier)
        elif stat == "lshield":
            modify_x_bits(buffer, offset + 39, 6, 0, value, modifier)
        else:
            raise UnknownAttributeError


def set_class_attribute(buffer, cls, attribute, value):
    offsets = ClassOffsets[LanguageUsed][0] + (ClassToIndex[cls] - 1) * 100, ClassOffsets[LanguageUsed][1] + (ClassToIndex[cls] - 1) * 100
    for offset in offsets:
        if attribute == "mount":
            v = MountStatus.index(value)
            write_x_bits(buffer, offset + 4, 2, 4, v)
        elif attribute == "type":
            v = UnitTypes.index(value)
            write_x_bits(buffer, offset + 4, 8, 7, 1 << v)
        elif attribute == "movement":
            v = MovementTypes.index(value)
            write_x_bits(buffer, offset + 6, 4, 1, v)
        else:
            raise UnknownAttributeError


def set_class_skill(buffer, cls, stat, value):
    wid = Skills.index(stat)
    offset = ClassOffsets[LanguageUsed][0] + (ClassToIndex[cls] - 1) * 100
    write_x_bits(buffer, offset + 12 + wid//8, 1, wid & 0x7, value)
    offset = ClassOffsets[LanguageUsed][1] + (ClassToIndex[cls] - 1) * 100
    write_x_bits(buffer, offset + 12 + wid // 8, 1, wid & 0x7, value)
