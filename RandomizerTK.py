
import tkinter as tk
import tkinter.font as tkFont
from RandomizerEditors import *


def clipboard_func(exported_string):
    try:
        pyperclip.copy(exported_string)
    except Exception:
        return


try:
    import pyperclip
except ImportError:
    clipboard_func = lambda exported_string: None


def main():

    window = tk.Tk()
    window.title("Berwick Saga Randomizer")
    window.resizable(height=False, width=False)

    title_font = tkFont.Font(family="Helvetica", size=24)
    ui_font = tkFont.Font(family="Helvetica", size=11)
    text_font = tkFont.Font(family="Monaco", size=11)

    randomize_bases = tk.BooleanVar(value=True)
    randomize_growths = tk.BooleanVar(value=True)
    randomize_wlv_bases = tk.BooleanVar(value=True)
    randomize_wlv_growths = tk.BooleanVar(value=True)
    randomize_skills = tk.BooleanVar(value=True)
    randomize_items = tk.BooleanVar(value=True)
    randomize_enemy_classes = tk.BooleanVar(value=True)
    zero_growths = tk.BooleanVar(value=False)
    zero_wlvl_growths = tk.BooleanVar(value=False)
    retrofit_stats = tk.BooleanVar(value=False)
    sherpa_bases = tk.BooleanVar(value=True)
    enid_magic = tk.BooleanVar(value=True)
    balanced_bases = tk.BooleanVar(value=True)
    balanced_growths = tk.BooleanVar(value=False)
    foot_unit_def_up = tk.BooleanVar(value=False)
    magic_unit_bulk_up = tk.BooleanVar(value=False)
    magic_unit_speed_up = tk.BooleanVar(value=False)
    thief_str_up = tk.BooleanVar(value=False)
    mag_is_everything = tk.BooleanVar(value=False)
    buff_wlv = tk.BooleanVar(value=False)
    use_skill_capacity = tk.BooleanVar(value=True)
    promotion_wlv = tk.BooleanVar(value=True)
    random_skills = tk.BooleanVar(value=False)
    random_skills2 = tk.BooleanVar(value=False)
    random_skills3 = tk.BooleanVar(value=False)
    random_breaker_skills = tk.BooleanVar(value=False)
    random_nasty_skills = tk.BooleanVar(value=False)
    exotic_weapon_buff = tk.BooleanVar(value=False)
    nerf_ballistae = tk.BooleanVar(value=False)
    nerf_lance_knights = tk.BooleanVar(value=False)
    four_move_priests = tk.BooleanVar(value=False)
    four_move_marcel = tk.BooleanVar(value=False)
    four_move_derrick = tk.BooleanVar(value=False)
    four_move_burroughs = tk.BooleanVar(value=False)
    hard_mode = tk.BooleanVar(value=False)
    lunatic_mode = tk.BooleanVar(value=False)
    enemy_stats_patch = tk.BooleanVar(value=False)
    anti_softlock_patch = tk.BooleanVar(value=False)
    robust_patch = tk.BooleanVar(value=False)
    unlimited_owen = tk.BooleanVar(value=False)

    stat_randomizer = tk.IntVar(value=0)
    level_randomizer = tk.IntVar(value=0)
    growth_randomizer = tk.IntVar(value=0)
    wlv_randomizer = tk.IntVar(value=0)
    skills_randomizer = tk.IntVar(value=0)
    learned_skills_randomizer = tk.IntVar(value=0)
    bracketing_randomizer = tk.IntVar(value=0)

    stat_min, stat_max = tk.StringVar(value="2"), tk.StringVar(value="2")
    level_variance = tk.StringVar(value="5")
    growth_variance = tk.StringVar(value="15")
    wlv_variance = tk.StringVar(value="5")
    wlv_growth_variance = tk.StringVar(value="30")
    wlv_growth_lower_cap = tk.StringVar(value="20")
    skill_keep_chance = tk.StringVar(value="0")
    weapon_damage_variance = tk.StringVar(value="1")
    weapon_hit_max = tk.StringVar(value="1")
    weapon_hit_min = tk.StringVar(value="1")
    weapon_cost_variance = tk.StringVar(value="500")
    weapon_durability_variance = tk.StringVar(value="1")
    weapon_weight_variance = tk.StringVar(value="1")
    weapon_level_variance = tk.StringVar(value="1")
    enemy_variance = tk.StringVar(value="1")
    enemy_stat_buff = tk.StringVar(value="2")
    treasure_price = tk.StringVar(value="5000")
    learned_skills = tk.StringVar(value="2")
    learned_skill_min = tk.StringVar(value="5")
    learned_skill_max = tk.StringVar(value="15")

    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    title_frame = tk.Frame(main_frame)
    title_frame.pack()
    tk.Label(title_frame, text="Berwick Saga Randomizer", font=title_font).pack()

    row_one = tk.Frame(main_frame)
    row_one.pack()

    player_frame = tk.LabelFrame(row_one, text="Players", font=text_font)
    player_frame.pack(side=tk.LEFT)

    tk.Label(player_frame, text="For Player Characters, Randomize:", font=text_font).pack(anchor=tk.W)
    tk.Checkbutton(player_frame, text="Bases", font=text_font, variable=randomize_bases).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(player_frame, text="Growths", font=text_font, variable=randomize_growths).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(player_frame, text="Weapon Level Bases", font=text_font, variable=randomize_wlv_bases).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(player_frame, text="Weapon Level Growths", font=text_font, variable=randomize_wlv_growths).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(player_frame, text="Skills", font=text_font, variable=randomize_skills).pack(anchor=tk.W, padx=20)
    tk.Label(player_frame, text="Randomize Characters Based On:", font=text_font).pack(anchor=tk.W)
    tk.Radiobutton(player_frame, text="Base Stats", font=text_font, variable=stat_randomizer, value=0).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(player_frame, text="Randomized Level", font=text_font, variable=stat_randomizer, value=1).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(player_frame, text="Joining Time", font=text_font, variable=stat_randomizer, value=2).pack(anchor=tk.W, padx=20)
    tk.Label(player_frame, text="Randomize Base Level:", font=text_font).pack(anchor=tk.W)
    tk.Radiobutton(player_frame, text="No", font=text_font, variable=level_randomizer, value=0).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(player_frame, text="Randomize", font=text_font, variable=level_randomizer, value=1).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(player_frame, text="Shuffle", font=text_font, variable=level_randomizer, value=2).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(player_frame, text="Retrofit Stats", font=text_font, variable=retrofit_stats).pack(anchor=tk.W, padx=10)

    player_frame_f1 = tk.Frame(player_frame)
    player_frame_f1.pack(anchor=tk.W, padx=10)
    tk.Label(player_frame_f1, text="Level Variance:", font=text_font).pack(side=tk.LEFT)
    mi = tk.Entry(player_frame_f1, textvariable=level_variance, width=10)
    mi.pack(side=tk.LEFT)

    tk.Checkbutton(player_frame, text="0% Growths", font=text_font, variable=zero_growths).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(player_frame, text="0% Weapon Level Growths", font=text_font, variable=zero_wlvl_growths).pack(anchor=tk.W, padx=20)

    growth_frame = tk.LabelFrame(row_one, text="Stats", font=text_font)
    growth_frame.pack(side=tk.LEFT)

    tk.Label(growth_frame, text="Bases Randomization:", font=text_font).pack(anchor=tk.W)

    growth_frame_f1 = tk.Frame(growth_frame)
    growth_frame_f1.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(growth_frame_f1, text="Max Increase:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(growth_frame_f1, textvariable=stat_max, width=11).pack(side=tk.LEFT)

    growth_frame_f2 = tk.Frame(growth_frame)
    growth_frame_f2.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(growth_frame_f2, text="Max Decrease:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(growth_frame_f2, textvariable=stat_min, width=11).pack(side=tk.LEFT)

    tk.Checkbutton(growth_frame, text="Try to Balance Base Stats", font=text_font, variable=balanced_bases).pack(anchor=tk.W, padx=10)
    tk.Checkbutton(growth_frame, text="Preserve Sherpa's Bulk", font=text_font, variable=sherpa_bases).pack(anchor=tk.W, padx=10)

    tk.Label(growth_frame, text="Growth Randomization based On:", font=text_font).pack(anchor=tk.W)
    tk.Radiobutton(growth_frame, text="Character Growth Rate", font=text_font, variable=growth_randomizer, value=0).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(growth_frame, text="Class Growth Rate", font=text_font, variable=growth_randomizer, value=1).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(growth_frame, text="Completely Randomized", font=text_font, variable=growth_randomizer, value=2).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(growth_frame, text="Preserve Enid's Magic", font=text_font, variable=enid_magic).pack(anchor=tk.W, padx=10)

    growth_frame_f3 = tk.Frame(growth_frame)
    growth_frame_f3.pack(anchor=tk.W, padx=10)
    tk.Label(growth_frame_f3, text="Growth Variance:", font=text_font).pack(side=tk.LEFT)
    mi = tk.Entry(growth_frame_f3, textvariable=growth_variance, width=8)
    mi.pack(side=tk.LEFT)

    tk.Checkbutton(growth_frame, text="Try to Balance Growth Rates", font=text_font, variable=balanced_growths).pack(anchor=tk.W, padx=10)

    tk.Label(growth_frame, text="Bracketing:", font=text_font).pack(anchor=tk.W)
    tk.Radiobutton(growth_frame, text="Don't Change", font=text_font, variable=bracketing_randomizer, value=0).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(growth_frame, text="Removed", font=text_font, variable=bracketing_randomizer, value=1).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(growth_frame, text="Randomized", font=text_font, variable=bracketing_randomizer, value=2).pack(anchor=tk.W, padx=20)

    tk.Label(growth_frame, text="Customization:", font=text_font).pack(anchor=tk.W)
    tk.Checkbutton(growth_frame, text="More Defense on Foot Units", font=text_font, variable=foot_unit_def_up).pack(anchor=tk.W, padx=10)
    tk.Checkbutton(growth_frame, text="More Bulk on Magic Users", font=text_font, variable=magic_unit_bulk_up).pack(anchor=tk.W, padx=10)
    tk.Checkbutton(growth_frame, text="More Speed on Magic Users", font=text_font, variable=magic_unit_speed_up).pack(anchor=tk.W, padx=10)
    tk.Checkbutton(growth_frame, text="More Strength on Thieves", font=text_font, variable=thief_str_up).pack(anchor=tk.W, padx=10)
    tk.Checkbutton(growth_frame, text="More Magic on Physical Units", font=text_font, variable=mag_is_everything).pack(anchor=tk.W, padx=10)

    skills_frame = tk.LabelFrame(row_one, text="Weapon Levels and Skills", font=text_font)
    skills_frame.pack(side=tk.LEFT)

    tk.Label(skills_frame, text="Weapon Level Randomized By:", font=text_font).pack(anchor=tk.W)
    tk.Radiobutton(skills_frame, text="Randomizing Original", font=text_font, variable=wlv_randomizer, value=0).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(skills_frame, text="Redistributing", font=text_font, variable=wlv_randomizer, value=1).pack(anchor=tk.W, padx=20)
    skills_frame_f1 = tk.Frame(skills_frame)
    skills_frame_f1.pack(anchor=tk.W, padx=20)
    tk.Radiobutton(skills_frame_f1, text="Shuffling", font=text_font, variable=wlv_randomizer, value=2).pack(side=tk.LEFT)
    tk.Checkbutton(skills_frame, text="Buff Low Base wlvs", font=text_font, variable=buff_wlv).pack(anchor=tk.W, padx=10)

    skills_frame_f2 = tk.Frame(skills_frame)
    skills_frame_f2.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(skills_frame_f2, text="Wlv Variance:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(skills_frame_f2, textvariable=wlv_variance, width=10).pack(side=tk.RIGHT)

    skills_frame_f3 = tk.Frame(skills_frame)
    skills_frame_f3.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(skills_frame_f3, text="Wlv Growth Variance:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(skills_frame_f3, textvariable=wlv_growth_variance, width=10).pack(side=tk.RIGHT)

    skills_frame_f4 = tk.Frame(skills_frame)
    skills_frame_f4.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(skills_frame_f4, text="Minimum Wlv Growth:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(skills_frame_f4, textvariable=wlv_growth_lower_cap, width=10).pack(side=tk.RIGHT)

    tk.Checkbutton(skills_frame, text="Promotion Friendly", font=text_font, variable=promotion_wlv).pack(anchor=tk.W, padx=10)

    tk.Label(skills_frame, text="How many skills?", font=text_font).pack(anchor=tk.W)
    tk.Radiobutton(skills_frame, text="Same as Original", font=text_font, variable=skills_randomizer, value=0).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(skills_frame, text="Randomized", font=text_font, variable=skills_randomizer, value=1).pack(anchor=tk.W, padx=20)
    tk.Radiobutton(skills_frame, text="Fill Everything", font=text_font, variable=skills_randomizer, value=2).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(skills_frame, text="Use Skill Capacity System", font=text_font, variable=use_skill_capacity).pack(anchor=tk.W, padx=10)

    skills_frame_f5 = tk.Frame(skills_frame)
    skills_frame_f5.pack(anchor=tk.W, padx=10)
    tk.Label(skills_frame_f5, text="Chance to Keep Skill:", font=text_font).pack(side=tk.LEFT)
    wlv = tk.Entry(skills_frame_f5, textvariable=skill_keep_chance, width=10)
    wlv.pack(side=tk.LEFT)

    tk.Label(skills_frame, text="Learned Skills:", font=text_font).pack(anchor=tk.W)
    tk.Radiobutton(skills_frame, text="Same Amount", font=text_font, variable=learned_skills_randomizer, value=0).pack(
        anchor=tk.W, padx=20)
    tk.Radiobutton(skills_frame, text="Convert To Innate", font=text_font, variable=learned_skills_randomizer, value=1).pack(
        anchor=tk.W, padx=20)
    skills_frame_f6 = tk.Frame(skills_frame)
    skills_frame_f6.pack(anchor=tk.W, padx=20)
    tk.Radiobutton(skills_frame_f6, text="Add Randomly, Max:", font=text_font, variable=learned_skills_randomizer, value=2).pack(side=tk.LEFT)
    tk.Entry(skills_frame_f6, textvariable=learned_skills, width=10).pack(side=tk.LEFT)

    skills_frame_f7 = tk.Frame(skills_frame)
    skills_frame_f7.pack(anchor=tk.W, padx=5)
    tk.Label(skills_frame_f7, text="Between Level", font=text_font).pack(side=tk.LEFT)
    tk.Entry(skills_frame_f7, textvariable=learned_skill_min, width=4).pack(side=tk.LEFT)
    tk.Label(skills_frame_f7, text="and", font=text_font).pack(side=tk.LEFT)
    tk.Entry(skills_frame_f7, textvariable=learned_skill_max, width=4).pack(side=tk.LEFT)

    frame4 = tk.Frame(row_one)
    frame4.pack(side=tk.LEFT)

    items_frame = tk.LabelFrame(frame4, text="Items and Classes", font=text_font)
    items_frame.pack()

    tk.Checkbutton(items_frame, text="Randomize Items", font=text_font, variable=randomize_items).pack(anchor=tk.W)

    items_frame_f1 = tk.Frame(items_frame)
    items_frame_f1.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(items_frame_f1, text="Damage Variance:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(items_frame_f1, textvariable=weapon_damage_variance, width=10).pack(side=tk.RIGHT)

    items_frame_f2 = tk.Frame(items_frame)
    items_frame_f2.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(items_frame_f2, text="Max Hit Increase:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(items_frame_f2, textvariable=weapon_hit_max, width=10).pack(side=tk.RIGHT)

    items_frame_f3 = tk.Frame(items_frame)
    items_frame_f3.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(items_frame_f3, text="Max Hit Decrease:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(items_frame_f3, textvariable=weapon_hit_min, width=10).pack(side=tk.RIGHT)

    items_frame_f4 = tk.Frame(items_frame)
    items_frame_f4.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(items_frame_f4, text="Cost Variance:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(items_frame_f4, textvariable=weapon_cost_variance, width=10).pack(side=tk.RIGHT)

    items_frame_f5 = tk.Frame(items_frame)
    items_frame_f5.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(items_frame_f5, text="Durability Variance:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(items_frame_f5, textvariable=weapon_durability_variance, width=10).pack(side=tk.RIGHT)

    items_frame_f6 = tk.Frame(items_frame)
    items_frame_f6.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(items_frame_f6, text="Weight Variance:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(items_frame_f6, textvariable=weapon_weight_variance, width=10).pack(side=tk.RIGHT)

    items_frame_f7 = tk.Frame(items_frame)
    items_frame_f7.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(items_frame_f7, text="Level Variance:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(items_frame_f7, textvariable=weapon_level_variance, width=10).pack(side=tk.RIGHT)

    tk.Checkbutton(items_frame, text="Randomize Enemies", font=text_font, variable=randomize_enemy_classes).pack(anchor=tk.W)

    items_frame_f9 = tk.Frame(items_frame)
    items_frame_f9.pack(anchor=tk.W, padx=10)
    tk.Label(items_frame_f9, text="Enemy Stat Variance:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(items_frame_f9, textvariable=enemy_variance, width=10).pack(side=tk.LEFT)

    items_frame_f10 = tk.Frame(items_frame)
    items_frame_f10.pack(anchor=tk.W, padx=20)
    tk.Checkbutton(items_frame_f10, text="Random Skills", font=text_font, variable=random_skills).pack(side=tk.LEFT)
    tk.Checkbutton(items_frame_f10, text="More", font=text_font, variable=random_skills2).pack(side=tk.LEFT)
    tk.Checkbutton(items_frame_f10, text="More", font=text_font, variable=random_skills3).pack(side=tk.LEFT)

    tk.Checkbutton(items_frame, text="Random Breaker Skills", font=text_font, variable=random_breaker_skills).pack(anchor=tk.W, padx=20)
    tk.Checkbutton(items_frame, text="Random Nasty Skills", font=text_font, variable=random_nasty_skills).pack(anchor=tk.W, padx=20)

    helper_frame = tk.LabelFrame(frame4, text="Helper Scripts", font=text_font)
    helper_frame.pack()

    tk.Checkbutton(helper_frame, text="More Exotic Weapon Uses", font=text_font, variable=exotic_weapon_buff).pack(anchor=tk.W, padx=10)
    tk.Checkbutton(helper_frame, text="Nerf Ballistae", font=text_font, variable=nerf_ballistae).pack(anchor=tk.W, padx=10)
    tk.Checkbutton(helper_frame, text="Nerf Lance Knights", font=text_font, variable=nerf_lance_knights).pack(anchor=tk.W, padx=10)

    helper_frame_f3 = tk.Frame(helper_frame)
    helper_frame_f3.pack(anchor=tk.W, padx=10)
    tk.Label(helper_frame_f3, text="Give 4 Move to:", font=text_font).pack(side=tk.LEFT, padx=5)
    tk.Checkbutton(helper_frame_f3, text="Priests", font=text_font, variable=four_move_priests).pack(side=tk.LEFT)

    helper_frame_f4 = tk.Frame(helper_frame)
    helper_frame_f4.pack(anchor=tk.W, padx=10)
    tk.Checkbutton(helper_frame_f4, text="Marcel", font=text_font, variable=four_move_marcel).pack(side=tk.LEFT)
    tk.Checkbutton(helper_frame_f4, text="Derrick", font=text_font, variable=four_move_derrick).pack(side=tk.LEFT)
    tk.Checkbutton(helper_frame_f4, text="Burroughs", font=text_font, variable=four_move_burroughs).pack(side=tk.LEFT)
    tk.Checkbutton(helper_frame, text="Remove Owen Limited", font=text_font, variable=unlimited_owen).pack(anchor=tk.W, padx=10)

    helper_frame_f1 = tk.Frame(helper_frame)
    helper_frame_f1.pack(anchor=tk.W, padx=10)
    tk.Checkbutton(helper_frame_f1, text="Hard Mode", font=text_font, variable=hard_mode).pack(side=tk.LEFT)
    tk.Checkbutton(helper_frame_f1, text="Lunatic Mode", font=text_font, variable=lunatic_mode).pack(side=tk.LEFT)

    helper_frame_f2 = tk.Frame(helper_frame)
    helper_frame_f2.pack(anchor=tk.W, padx=10)
    tk.Checkbutton(helper_frame_f2, text="Increase Enemy Stats by:", font=text_font, variable=enemy_stats_patch).pack(side=tk.LEFT)
    es = tk.Entry(helper_frame_f2, textvariable=enemy_stat_buff, width=6)
    es.pack(side=tk.LEFT)
    tk.Checkbutton(helper_frame, text="Vulneraries on Guest Units", font=text_font, variable=anti_softlock_patch).pack(anchor=tk.W, padx=10)
    tk.Checkbutton(helper_frame, text="Robust+ on All Players", font=text_font, variable=robust_patch).pack(anchor=tk.W, padx=10)

    helper_frame_f8 = tk.Frame(helper_frame)
    helper_frame_f8.pack(anchor=tk.W, padx=10, fill=tk.X, expand=True)
    tk.Label(helper_frame_f8, text="Treasure Sells For:", font=text_font).pack(side=tk.LEFT)
    tk.Entry(helper_frame_f8, textvariable=treasure_price, width=10).pack(side=tk.RIGHT)

    row_two = tk.Frame(main_frame)
    row_two.pack()

    def generate():
        buffer = ""
        buffer += include_file(exotic_weapon_buff.get(), nerf_ballistae.get(), nerf_lance_knights.get(), four_move_priests.get(), four_move_marcel.get(), four_move_derrick.get(), four_move_burroughs.get(), unlimited_owen.get(),
                     hard_mode.get(), lunatic_mode.get(), enemy_stats_patch.get(), int(enemy_stat_buff.get()), anti_softlock_patch.get(), robust_patch.get(), int(treasure_price.get()))
        buffer += base_randomization(randomize_bases.get(), randomize_wlv_bases.get(), stat_randomizer.get(), level_randomizer.get(), int(level_variance.get()),
                           retrofit_stats.get(), int(stat_max.get()), int(stat_min.get()), balanced_bases.get(), sherpa_bases.get(), wlv_randomizer.get(), int(wlv_variance.get()), buff_wlv.get())
        if randomize_bases.get():
            buffer += base_adjustment(foot_unit_def_up.get(), magic_unit_bulk_up.get(), magic_unit_speed_up.get(), thief_str_up.get(), mag_is_everything.get())
        if zero_growths.get():
            buffer += zero_percent_growth()
        elif randomize_growths.get():
            buffer += growth_randomization(growth_randomizer.get(), int(growth_variance.get()), balanced_growths.get(), enid_magic.get())
            buffer += growth_adjustment(growth_randomizer.get(), foot_unit_def_up.get(), magic_unit_bulk_up.get(), magic_unit_speed_up.get(), thief_str_up.get(), mag_is_everything.get())
        if zero_wlvl_growths.get():
            buffer += zero_weapon_rank_growth()
        elif randomize_wlv_growths.get():
            buffer += wlv_growth_randomization(wlv_randomizer.get(), int(wlv_growth_variance.get()), int(wlv_growth_lower_cap.get()), promotion_wlv.get())
        if randomize_skills.get():
            buffer += skills_randomization(skills_randomizer.get(), use_skill_capacity.get(), int(skill_keep_chance.get()),
                                           learned_skills_randomizer.get(), int(learned_skills.get()), int(learned_skill_min.get()), int(learned_skill_max.get()))
        if randomize_items.get():
            buffer += items_randomization(int(weapon_damage_variance.get()), int(weapon_hit_max.get()), int(weapon_hit_min.get()),
                                int(weapon_cost_variance.get()), int(weapon_durability_variance.get()), int(weapon_level_variance.get()), int(weapon_weight_variance.get()))
        if randomize_enemy_classes.get():
            buffer += enemy_class_randomization(int(enemy_variance.get()), random_skills.get(), random_skills2.get(), random_skills3.get(), random_breaker_skills.get(), random_nasty_skills.get())
        buffer += bracketing_randomization(bracketing_randomizer.get())
        new_window = tk.Toplevel(window)
        new_window.title("Output")
        new_window.resizable(height=False, width=False)
        script_box = tk.Text(new_window)
        script_box.insert("1.0", buffer)
        script_box.pack()
        script_box.bind('<Control-a>', lambda x: script_box.tag_add("sel", '0.0', 'end'))
        script_box.bind('<Command-a>', lambda x: script_box.tag_add("sel", '0.0', 'end'))
        copy_button = tk.Button(new_window, text="Copy", font=ui_font, command=lambda: clipboard_func(script_box.get("1.0", "end")))
        copy_button.pack()
        new_window.mainloop()
    randomize_button = tk.Button(row_two, text="Randomize!", font=ui_font, command=generate)
    randomize_button.pack()

    def unset_randomizers():
        randomize_bases.set(False)
        randomize_growths.set(False)
        randomize_wlv_bases.set(False)
        randomize_wlv_growths.set(False)
        randomize_skills.set(False)
        randomize_items.set(False)
        randomize_enemy_classes.set(False)
        level_randomizer.set(0)
        bracketing_randomizer.set(0)

    dont_randomize_button = tk.Button(player_frame, text="Unset All Randomizers", font=ui_font, command=unset_randomizers)
    dont_randomize_button.pack()

    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)
    window.mainloop()


if __name__ == '__main__':
    main()
