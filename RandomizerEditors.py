import random
import math
from BWSDefinitions import *
from RandomizerDefinitions import *


def splitvalue(value, slices):
    n = sorted([random.randint(0, value) for i in range(slices - 1)])
    last = 0
    result = []
    for i in n:
        result.append(i - last)
        last = i
    result.append(value - last)
    return result


def sign_str(v):
    return "+" if v >= 0 else "-"


def fit(value, min, max):
    return max if value > max else min if value < min else value


def fit_mid(value, min, max):
    return (max + min) // 2 if value > (max + min) // 2 else (max + min) // 2 if value < min else value


def autolevel_with_growth(levels, growth):
    autolevel = abs(levels * growth)
    return math.copysign(autolevel // 100 + (1 if random.randint(0, 99) < autolevel % 100 else 0), levels * growth)


def linear_variance(max_dec, max_inc):
    return random.randint(-max_dec, max_inc)


def balanced_linear_variance(max_dec, max_inc, bias=5):
    if random.randint(0, 9) < bias:
        return -random.randint(0, max_dec)
    else:
        return random.randint(0, max_inc)


def balanced_triangular_variance(max_dec, max_inc, mode, bias=5):
    if random.randint(0, 9) < bias:
        return -int(random.triangular(0, max_dec + 1, fit_mid(mode, 0, max_dec)))
    else:
        return int(random.triangular(0, max_inc + 1, fit_mid(mode, 0, max_inc)))


def include_file(exotic_weapon_buff, nerf_ballistae, nerf_lance_knights, four_move_priests, four_move_marcel, four_move_derrick, four_move_burroughs, unlimited_owen, hard_mode, lunatic_mode, enemy_stats_patch, enemy_stat_buff, vulneries_patch, robust_patch, treasure_price):
    buffer = ""
    if exotic_weapon_buff:
        buffer += "import exotic_weapon_uses\n"
    if nerf_ballistae:
        buffer += "import nerf_ballistae\n"
    if nerf_lance_knights:
        buffer += "import nerf_lance_knights\n"
    if four_move_priests:
        buffer += "import four_move_priests\n"
    if hard_mode:
        buffer += "import hard\n"
    if lunatic_mode:
        buffer += "import lunatic\n"
    if enemy_stats_patch:
        buffer += "import enemy+{}\n".format(fit(enemy_stat_buff, 1, 5))
    if vulneries_patch:
        buffer += "import vulneries\n"
    if robust_patch:
        buffer += "import robust_players\n"
    if four_move_marcel:
        buffer += "unset marcel skill slowstart\n"
    if four_move_derrick:
        buffer += "set derrick skill celerity\n"
    if four_move_burroughs:
        buffer += "set burroughs skill celerity\n"
    if unlimited_owen:
        buffer += "unset RazeMonkOwen skill limited\n"
    if treasure_price != 5000:
        buffer += "set Treasure stat price {}\n".format(treasure_price * 2)
    return buffer


def base_randomization(randomize_bases, randomize_wlv_bases, stat_randomizer, level_randomizer, level_variance,
                       retrofit_stats, stat_max, stat_min, balanced_bases, sherpa_bases, wlv_randomizer, wlv_variance, buff_wlv):
    stats = ["strength", "magic", "defense", "speed", "hp"]
    buffer = ""
    shuffled_levels = [BaseLevel[i] for i in BaseLevel]
    random.shuffle(shuffled_levels)
    for index, unit in enumerate(UnitToOffset):
        orig_level = BaseLevel[unit]
        level = orig_level
        if level_randomizer == 1:
            level = fit(orig_level + balanced_linear_variance(level_variance, level_variance), 1, 30)
        elif level_randomizer == 2:
            level = shuffled_levels[index]
        if stat_randomizer == 0:
            internal_level = orig_level
        elif stat_randomizer == 1:
            internal_level = level
        elif stat_randomizer == 2:
            internal_level = JoiningChapter[unit] * 22 // 15
            internal_level += fit((orig_level - internal_level - 8) * 2, 0, 20)  # gives jagens a bit more levels
        delta_stats = 0
        # auto-level
        if randomize_bases:
            for stat in stats:
                if unit == "sherpa" and (stat == "hp" or stat == "defense") and sherpa_bases:
                    continue
                autolevel = autolevel_with_growth(internal_level - orig_level, GenericGrowth[stat])
                if balanced_bases:
                    random_bonus = balanced_triangular_variance(stat_min, stat_max, 2, 5 + delta_stats)
                else:
                    random_bonus = balanced_linear_variance(stat_min, stat_max)
                if (stat == "defense" and unit not in ArmoredUnits) or (stat == "magic" and unit not in MagicUsers):
                    random_bonus = (random_bonus + 1) // 2  # round up for fun
                delta_stats += random_bonus
                if autolevel + random_bonus != 0:
                    if unit != "reese" or autolevel + random_bonus > 0:
                        buffer += "set {} base {} {}{:.0f}\n".format(unit, stat, sign_str(autolevel + random_bonus), abs(autolevel + random_bonus))
                    else:  # reese has 0 personal bases, so we change his class
                        buffer += "set Lord_R base {} -{:.0f}\n".format(stat, abs(autolevel + random_bonus))
                        buffer += "set Lord base {} -{:.0f}\n".format(stat, abs(autolevel + random_bonus))
                        buffer += "set KnightLord_R base {} -{:.0f}\n".format(stat, abs(autolevel + random_bonus))
                        buffer += "set KnightLord base {} -{:.0f}\n".format(stat, abs(autolevel + random_bonus))

        if retrofit_stats:
            internal_level += delta_stats * StatToLevelConstant
            buffer += "set {} base level {:.0f}\n".format(unit, internal_level)
        elif level_randomizer != 0:
            buffer += "set {} base level {:.0f}\n".format(unit, level)
        if randomize_wlv_bases:
            if wlv_randomizer == 0:
                for weapon in WeaponLevels[unit]:
                    base, _ = WeaponLevels[unit][weapon]
                    if base != 0:
                        random_bonus = balanced_linear_variance(wlv_variance, wlv_variance)
                        autolevel = autolevel_with_growth(internal_level - orig_level, 50)
                        base = fit(base + random_bonus + autolevel, 0, 40)
                        if buff_wlv and base < 10:
                            base = fit(int(base * 1.5 + 2), 5, 10)
                        buffer += "set {} base {} {:.0f}\n".format(unit, weapon, fit(base, 0, 40))
            elif wlv_randomizer == 1:
                sum_wlv = sum([WeaponLevels[unit][w][0] for w in WeaponLevels[unit]])
                weapons = [w for w in WeaponLevels[unit] if WeaponLevels[unit][w][0] != 0]
                bases = splitvalue(sum_wlv, len(weapons))
                for i, weapon in enumerate(weapons):
                    base = fit(bases[i] + autolevel_with_growth(internal_level - orig_level, 50), 0, 50)
                    if buff_wlv and base < 10:
                        base = fit(int(base * 1.5 + 2), 5, 10)
                    buffer += "set {} base {} {:.0f}\n".format(unit, weapon, base)
            else:
                weapons = [w for w in WeaponLevels[unit] if WeaponLevels[unit][w][0] != 0]
                bases = [WeaponLevels[unit][w][0] for w in WeaponLevels[unit] if WeaponLevels[unit][w][0] != 0]
                random.shuffle(bases)
                for i, weapon in enumerate(weapons):
                    random_bonus = balanced_linear_variance(wlv_variance, wlv_variance)
                    base = fit(bases[i] + random_bonus + autolevel_with_growth(internal_level - orig_level, 50), 0, 40)
                    if buff_wlv and base < 10:
                        base = fit(int(base * 1.5 + 2), 5, 10)
                    buffer += "set {} base {} {:.0f}\n".format(unit, weapon, base)
    return buffer


def base_adjustment(foot_unit_def_up, magic_unit_bulk_up, magic_unit_speed_up, thief_str_up, mag_is_everything):
    buffer = ""
    if foot_unit_def_up:
        for unit in LightFootUnits:
            n = random.randint(-3, 3)
            if n > 0:
                buffer += "set {} base defense +{}\n".format(unit, n)
    if magic_unit_bulk_up:
        for unit in MagicUnits:
            n = random.randint(-3, 3)
            if n > 0:
                buffer += "set {} base defense +{}\n".format(unit, n)
            n = random.randint(-1, 3)
            if n > 0:
                buffer += "set {} base hp +{}\n".format(unit, n)
    if magic_unit_speed_up:
        for unit in MagicUnits:
            n = random.randint(0, 3)
            if n > 0:
                buffer += "set {} base speed +{}\n".format(unit, n)
    if thief_str_up:
        for unit in ThiefUnits:
            n = random.randint(0, 5)
            if n > 0:
                buffer += "set {} base strength +{}\n".format(unit, n)
    if mag_is_everything:
        for unit in PhysicalUnits:
            n = random.randint(-6, 3)
            if n > 0:
                buffer += "set {} base magic +{}\n".format(unit, n)
    return buffer


def growth_randomization(growth_randomizer, growth_variance, balanced_growths, enid_magic):
    stats = ["strength", "magic", "defense", "speed", "hp"]
    buffer = ""
    for index, unit in enumerate(UnitToOffset):
        bias = 0
        for stat in stats:
            if growth_randomizer == 0:  # wtf is 1 supposed to be again
                v = growth_variance
                if stat == "defense" or stat == "magic":
                    v = (v + 1) // 2  # round up for fun
                if balanced_growths:
                    random_bonus = balanced_linear_variance(v, v, 5 + bias)
                else:
                    random_bonus = balanced_linear_variance(v, v)
                if enid_magic and stat == "magic" and unit.lower() == "enid":
                    random_bonus = max(0, random_bonus)
                bias += random_bonus / 20
                if random_bonus != 0:
                    buffer += "set {} growth {} {}{:.0f}\n".format(unit, stat, sign_str(random_bonus), abs(random_bonus))
            elif growth_randomizer == 1:
                v = growth_variance
                if stat == "defense" or stat == "magic":
                    v = (v + 1) // 2  # round up for fun
                if unit in ThiefUnits:
                    value = fit(ThiefGrowth[stat] // 2 + balanced_linear_variance(v, v), 0, 60)
                elif unit in LightFootUnits:
                    value = fit(LightUnitGrowth[stat] // 2 + balanced_linear_variance(v, v), 0, 60)
                elif unit in MagicUnits:
                    value = fit(MagicUnitGrowth[stat] // 2 + balanced_linear_variance(v, v), 0, 60)
                else:
                    value = fit(HeavyUnitGrowth[stat] // 2 + balanced_linear_variance(v, v), 0, 60)
                if enid_magic and stat == "magic" and unit.lower() == "enid":
                    value = fit(value, 20, 60)
                buffer += "set {} growth {} {:.0f}\n".format(unit, stat, value)
            elif growth_randomizer == 2:
                if enid_magic and stat == "magic" and unit.lower() == "enid":
                    buffer += "set {} growth {} {:.0f}\n".format(unit, stat, fit(random.randint(0, MagicUnitGrowth[stat]), 20, MagicUnitGrowth[stat]))
                elif unit in ThiefUnits:
                    buffer += "set {} growth {} {:.0f}\n".format(unit, stat, random.randint(0, ThiefGrowth[stat]))
                elif unit in LightFootUnits:
                    buffer += "set {} growth {} {:.0f}\n".format(unit, stat, random.randint(0, LightUnitGrowth[stat]))
                elif unit in MagicUnits:
                    buffer += "set {} growth {} {:.0f}\n".format(unit, stat, random.randint(0, MagicUnitGrowth[stat]))
                else:
                    buffer += "set {} growth {} {:.0f}\n".format(unit, stat, random.randint(0, HeavyUnitGrowth[stat]))
    return buffer


def growth_adjustment(growth_randomizer, foot_unit_def_up, magic_unit_bulk_up, magic_unit_speed_up,thief_str_up, mag_is_everything):
    if growth_randomizer == 2:
        return ""  # completely randomized, don't need
    buffer = ""
    if foot_unit_def_up:
        for unit in LightFootUnits:
            n = random.randint(-6, 12)
            if n > 0:
                buffer += "set {} growth defense +{}\n".format(unit, n)
    if magic_unit_bulk_up:
        for unit in MagicUnits:
            n = random.randint(-6, 12)
            if n > 0:
                buffer += "set {} growth defense +{}\n".format(unit, n)
            n = random.randint(-6, 12)
            if n > 0:
                buffer += "set {} growth hp +{}\n".format(unit, n)
    if magic_unit_speed_up:
        for unit in MagicUnits:
            n = random.randint(-5, 15)
            if n > 0:
                buffer += "set {} growth speed +{}\n".format(unit, n)
    if thief_str_up:
        for unit in ThiefUnits:
            n = random.randint(0, 30)
            if n > 0:
                buffer += "set {} growth strength +{}\n".format(unit, n)
    if mag_is_everything:
        for unit in PhysicalUnits:
            n = random.randint(-20, 20)
            if n > 0:
                buffer += "set {} growth magic +{}\n".format(unit, n)
    return buffer


def wlv_growth_randomization(wlv_randomizer, wlv_growth_variance, wlv_growth_lower_cap, promotion_wlv):
    buffer = ""
    for index, unit in enumerate(UnitToOffset):
        if wlv_randomizer == 0:
            for weapon in WeaponLevels[unit]:
                _, growth = WeaponLevels[unit][weapon]
                if growth != 0:
                    random_bonus = balanced_linear_variance(wlv_growth_variance, wlv_growth_variance)
                    growth = fit(growth + random_bonus, wlv_growth_lower_cap, 90)
                    if promotion_wlv and weapon in PromoGuard[unit] and PromoGuard[unit][weapon] > growth:
                        growth = PromoGuard[unit][weapon]
                    buffer += "set {} growth {} {}\n".format(unit, weapon, abs(growth))
        elif wlv_randomizer == 1:
            sum_wlv_growth = sum([WeaponLevels[unit][w][1] for w in WeaponLevels[unit]])
            weapons = [w for w in WeaponLevels[unit] if WeaponLevels[unit][w][1] != 0]
            growths = splitvalue(sum_wlv_growth, len(weapons))
            for i, weapon in enumerate(weapons):
                growth = fit(growths[i], wlv_growth_lower_cap, 90)
                if promotion_wlv and weapon in PromoGuard[unit] and PromoGuard[unit][weapon] > growth:
                    growth = PromoGuard[unit][weapon]
                buffer += "set {} growth {} {}\n".format(unit, weapon, growth)
        else:
            weapons = [w for w in WeaponLevels[unit] if WeaponLevels[unit][w][1] != 0]
            growths = [WeaponLevels[unit][w][1] for w in WeaponLevels[unit] if WeaponLevels[unit][w][1] != 0]
            random.shuffle(growths)
            for i, weapon in enumerate(weapons):
                random_bonus = balanced_linear_variance(wlv_growth_variance, wlv_growth_variance)
                growth = fit(growths[i] + random_bonus, wlv_growth_lower_cap, 90)
                if promotion_wlv and weapon in PromoGuard[unit] and PromoGuard[unit][weapon] > growth:
                    growth = PromoGuard[unit][weapon]
                buffer += "set {} growth {} {}\n".format(unit, weapon, growth)
    return buffer


def skills_randomization(skills_editor, use_skill_capacity, skill_keep_chance,
                         learned_skills_randomizer, num_skills_learned, learned_skill_min, learned_skill_max):
    buffer = ""
    cheap_skills = [s for s in SkillCapacity if SkillCapacity[s] == 1]
    expensive_skills = [s for s in SkillCapacity if SkillCapacity[s] > 1]
    buffer += "set {} skill {}\n".format("reese", "robust2")
    buffer += "set {} skill {}\n".format("ward", "robust2")
    for unit in UnitToOffset:
        skills_added = 0
        locked_capacity = DefaultSkillCapacity[unit] - len(RemovableSkills[unit])
        max_capacity = DefaultSkillCapacity[unit]
        if learned_skills_randomizer == 1:
            max_capacity += LearnedSkills[unit]  # convert learned skills to innate skills, don't add bonus capacity
        bonus_capacity = 0
        for skill in RemovableSkills[unit]:
            if random.randint(0, 99) > skill_keep_chance:
                buffer += "unset {} skill {}\n".format(unit, skill)
                bonus_capacity += SkillCapacity[skill] - 1
            else:
                skills_added += 1
        if skills_editor == 1:
            b = balanced_linear_variance(3, 3)
            max_capacity = fit(max_capacity + b, locked_capacity, 7)
            bonus_capacity = fit(bonus_capacity + b, 0, 10)
        elif skills_editor == 2:
            max_capacity = 7
        legal_skills = [s for s in SkillLegality if SkillLegality[s] is True or isinstance(SkillLegality[s], list) and unit in SkillLegality[s]]
        legal_skills_e = [s for s in expensive_skills if s in legal_skills]
        legal_skills_c = [s for s in cheap_skills if s in legal_skills]
        learned = []
        if not use_skill_capacity:
            bonus_capacity = 99 # ignored basically
        while max_capacity > locked_capacity + skills_added:
            if use_skill_capacity and bonus_capacity > 2 and len(legal_skills_e) > 3:  # Maybe Edit this number
                new_skill = random.choice(legal_skills_e)
            elif use_skill_capacity and bonus_capacity == 0:
                new_skill = random.choice(legal_skills_c)
            else:
                new_skill = random.choice(legal_skills_e + legal_skills_c)
            if SkillCapacity[new_skill] - 1 <= bonus_capacity and new_skill not in learned:
                skills_added += 1
                bonus_capacity -= SkillCapacity[new_skill] - 1
                buffer += "set {} skill {}\n".format(unit, new_skill)
                learned.append(new_skill)
        learned_pool = legal_skills_c + legal_skills_c + legal_skills_e
        min_lv = learned_skill_min
        if learned_skills_randomizer == 1:
            num = 0
        elif learned_skills_randomizer == 0:
            num = LearnedSkills[unit]
        else:
            num = random.randint(0, num_skills_learned)
        num = fit(num, 0, 7 - max_capacity)
        if num < LearnedSkills[unit]:
            for i in range(num, LearnedSkills[unit]):
                buffer += "unset {} learned {}\n".format(unit, i)
        for i in range(num):
            level = random.randint(min_lv, learned_skill_max - (num - i))
            new_skill = ""
            while new_skill == "" or new_skill in learned:
                new_skill = random.choice(learned_pool)
            buffer += "set {} learned {} {} {}\n".format(unit, i, new_skill, level)
            min_lv = level + 1
            learned.append(new_skill)

    return buffer


def items_randomization(weapon_damage_variance, weapon_hit_max, weapon_hit_min, weapon_cost_variance, weapon_durability_variance, weapon_level_variance, weapon_weight_variance):
    buffer = ""
    for item in ItemToIndex:
        if ItemToIndex[item] <= WeaponEnd and "dummy" not in item and "broken" not in item:
            if ItemToIndex[item] in range(HealOrbsStart, OrbsEnd):
                continue
            dmg = linear_variance(weapon_damage_variance, weapon_damage_variance)
            hit = linear_variance(weapon_hit_min, weapon_hit_max)
            cost = linear_variance(weapon_cost_variance, weapon_cost_variance)
            durability = linear_variance(weapon_durability_variance, weapon_durability_variance)
            weight = linear_variance(weapon_weight_variance, weapon_weight_variance)
            level = linear_variance(weapon_level_variance, weapon_level_variance)
            if dmg != 0:
                buffer += "set {} stat might {}{}\n".format(item, sign_str(dmg), abs(dmg))
            if hit != 0:
                buffer += "set {} stat accuracy {}{}\n".format(item, sign_str(hit), abs(hit) * 10)
            if cost != 0:
                buffer += "set {} stat cost {}{}\n".format(item, sign_str(cost), abs(cost))
            if durability != 0:
                if ItemToIndex[item] in range(OrbsStart, HealOrbsStart):
                    buffer += "set {} stat uses {}{}\n".format(item, sign_str(durability), abs(durability) * 4)
                else:
                    buffer += "set {} stat durability {}{}\n".format(item, sign_str(durability), abs(durability))
            if weight != 0:
                buffer += "set {} stat weight {}{}\n".format(item, sign_str(weight), abs(weight))
            if level != 0:
                buffer += "set {} stat level {}{}\n".format(item, sign_str(level), abs(level))

    return buffer


def enemy_class_randomization(enemy_variance, random_skills, random_skills2, random_skills3, random_breaker_skills, random_nasty_skills):
    buffer = ""
    stats = ["strength", "magic", "defense", "speed", "hp"]
    for cl in EnemyClasses:
        for stat in stats:
            n = linear_variance(enemy_variance, enemy_variance)
            if stat == "magic" and cl in ArmoredEnemies:
                n = max(0, n)
            elif stat == "magic" and cl not in MagicalEnemies:
                n //= 2
            elif stat == "defense" and cl not in ArmoredEnemies:
                n //= 2
            if n != 0:
                buffer += "set {} base {} {}{}\n".format(cl, stat, sign_str(n), abs(n))
        for _ in range(sum((random_skills, random_skills2, random_skills3))):
            buffer += "set {} skill {}\n".format(cl, random.choice(EnemySkillSet1))
        if random_breaker_skills:
            if cl in ArmoredEnemies:
                buffer += "set {} skill {}\n".format(cl, random.choice(EnemySkillSet3[:-1]))
            else:
                buffer += "set {} skill {}\n".format(cl, random.choice(EnemySkillSet3))
        if random_nasty_skills:
                buffer += "set {} skill {}\n".format(cl, random.choice(EnemySkillSet2))
    return buffer


def bracketing_randomization(randomizer):
    buffer = ""
    if randomizer == 0:
        return buffer
    elif randomizer == 1:
        for unit in UnitToOffset:
            buffer += "set {} bracket no\n".format(unit)
    else:
        for unit in UnitToOffset:
            buffer += "set {} bracket {}\n".format(unit, random.choice(("no", "tight", "loose")))
    return buffer


def zero_percent_growth():
    buffer = ""
    stats = ["strength", "magic", "defense", "speed", "hp"]
    for unit in UnitToOffset:
        for stat in stats:
            buffer += "set {} growth {} {}\n".format(unit, stat, 0)
    return buffer


def zero_weapon_rank_growth():
    buffer = ""
    for unit in UnitToOffset:
        for stat in WeaponLevels[unit]:
            if stat not in ("sshield", "mshield", "lshield"):
                buffer += "set {} growth {} {}\n".format(unit, stat, 0)
    return buffer
