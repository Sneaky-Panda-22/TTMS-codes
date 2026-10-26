"""
TTMS (Gear & Setup) - sample data generator
Prepared with assistance from Claude; adapted for the final TTMS database name.
Writes ttms_seed_data.sql containing batched INSERT statements for:
Player, Blade, Rubber, Glue, Setup  (in FK-safe order).

Usage:   pip install faker
         python generate_ttms_data.py
Then in MySQL:   SOURCE ttms_seed_data.sql;
"""

import random
from datetime import datetime, timedelta
from faker import Faker

SEED = 42
random.seed(SEED)
fake = Faker("en_IN")
Faker.seed(SEED)

OUT_FILE = "ttms_seed_data.sql"
BATCH = 500

N_PLAYERS = 2200
N_SETUPS = 4000          # blades + rubbers + glues add ~250 more rows on top

# ------------------------------------------------------------
# Catalog data (brand, model, tag, ...). tag = which play style the
# item suits: off = offensive, all = all_round, def = defensive.
# ------------------------------------------------------------

# (brand, model, material, plies, base_weight_g, base_price_inr, tag)
BLADE_BASES = [
    ("Butterfly", "Viscaria", "Arylate-Carbon", 7, 88, 15500, "off"),
    ("Butterfly", "Timo Boll ALC", "ALC", 7, 87, 14000, "off"),
    ("Butterfly", "Innerforce Layer ALC", "ALC", 7, 86, 13500, "off"),
    ("Butterfly", "Garaydia ALC", "ALC", 7, 87, 12500, "off"),
    ("Butterfly", "Zhang Jike Super ZLC", "ZLC", 7, 89, 16500, "off"),
    ("Butterfly", "Petr Korbel", "Wood", 5, 85, 6500, "all"),
    ("Butterfly", "Primorac", "Wood", 5, 84, 7000, "all"),
    ("Stiga", "Clipper CR WRB", "Wood", 5, 89, 6500, "off"),
    ("Stiga", "Offensive Classic", "Wood", 5, 87, 4500, "off"),
    ("Stiga", "Carbonado 45", "Carbon", 7, 86, 9500, "off"),
    ("Stiga", "Cybershape Carbon", "Carbon", 7, 85, 10000, "off"),
    ("Stiga", "Allround Classic", "Wood", 5, 85, 4000, "all"),
    ("Stiga", "Defensive Classic", "Wood", 5, 86, 4200, "def"),
    ("DHS", "Hurricane Long 5", "Wood", 5, 88, 4200, "off"),
    ("DHS", "Power G7", "Carbon", 7, 86, 5500, "off"),
    ("DHS", "Hurricane 301", "Wood", 5, 87, 3500, "off"),
    ("Yasaka", "Ma Lin Extra Offensive", "Wood", 5, 87, 6000, "off"),
    ("Yasaka", "Mark V", "Wood", 5, 85, 3800, "all"),
    ("Yasaka", "Sweden Extra", "Wood", 5, 86, 4500, "all"),
    ("Donic", "Waldner Senso Carbon", "Carbon", 7, 87, 9000, "off"),
    ("Donic", "Persson Powerplay", "Wood", 5, 86, 7500, "off"),
    ("Donic", "Appelgren Allplay", "Wood", 5, 85, 5500, "all"),
    ("Donic", "Defplay Senso", "Wood", 5, 86, 6500, "def"),
    ("Nittaku", "Acoustic Carbon", "Carbon", 7, 88, 11000, "off"),
    ("Tibhar", "Stratus Power Wood", "Wood", 5, 89, 7500, "off"),
    ("Tibhar", "Samsonov Force Pro", "Wood", 5, 88, 8000, "off"),
]
HANDLES = {"FL": 0, "ST": 2, "CS": 1, "AN": 1, "PEN": -3}   # handle -> weight offset (g)

# (brand, model, tag, base_price_inr)
RUBBER_BASES = [
    ("Butterfly", "Tenergy 05", "off", 4800), ("Butterfly", "Tenergy 05 FX", "off", 4800),
    ("Butterfly", "Tenergy 05 Hard", "off", 4900), ("Butterfly", "Tenergy 64", "off", 4600),
    ("Butterfly", "Tenergy 64 FX", "all", 4600), ("Butterfly", "Tenergy 80", "off", 4800),
    ("Butterfly", "Tenergy 80 FX", "all", 4800), ("Butterfly", "Dignics 05", "off", 5500),
    ("Butterfly", "Dignics 09C", "off", 5500), ("Butterfly", "Dignics 64", "off", 5300),
    ("Butterfly", "Dignics 80", "off", 5400), ("Butterfly", "Rozena", "off", 3200),
    ("Butterfly", "Sriver", "all", 2800), ("Butterfly", "Sriver FX", "all", 2800),
    ("Butterfly", "Glayzer", "all", 3000), ("Butterfly", "Glayzer 09C", "off", 3400),
    ("Butterfly", "Feint Long III", "def", 2300), ("Butterfly", "Tackiness Chop", "def", 2800),
    ("DHS", "Hurricane 3", "off", 2800), ("DHS", "Hurricane 3 Neo", "off", 3000),
    ("DHS", "Hurricane 8", "off", 3300), ("DHS", "Skyline 3", "off", 2500),
    ("DHS", "Skyline 3 Neo", "off", 2700), ("DHS", "Goldarc 8", "off", 2600),
    ("Yasaka", "Rakza 7", "off", 3600), ("Yasaka", "Rakza 7 Soft", "all", 3600),
    ("Yasaka", "Rakza Z", "off", 3800), ("Yasaka", "Rakza X", "off", 3900),
    ("Yasaka", "Rakza 9", "off", 3800), ("Yasaka", "Mark V", "all", 2800),
    ("Donic", "Bluefire M1", "off", 3400), ("Donic", "Bluefire M2", "off", 3400),
    ("Donic", "Bluefire M3", "all", 3400), ("Donic", "Acuda S1", "off", 3300),
    ("Donic", "Acuda S2", "off", 3300), ("Donic", "Baracuda", "off", 3000),
    ("Xiom", "Vega Pro", "off", 2600), ("Xiom", "Vega Asia", "off", 2600),
    ("Xiom", "Vega Europe", "all", 2600), ("Xiom", "Omega VII Pro", "off", 4000),
    ("Xiom", "Omega VII Asia", "off", 4000), ("Xiom", "Omega VII Euro", "all", 4000),
    ("Nittaku", "Fastarc G-1", "off", 4500), ("Nittaku", "Moristo SP", "all", 3000),
    ("Nittaku", "Fastarc P-1", "off", 4300),
    ("Andro", "Rasanter R42", "off", 3400), ("Andro", "Rasanter R47", "off", 3600),
    ("Andro", "Rasanter R53", "off", 3700), ("Andro", "Hexer", "off", 3400),
    ("Andro", "Hexer Grip", "off", 3500), ("Andro", "Rasant Powergrip", "off", 3300),
    ("Tibhar", "Evolution MX-P", "off", 4200), ("Tibhar", "Evolution MX-S", "off", 4200),
    ("Tibhar", "Evolution FX-P", "all", 4100), ("Tibhar", "Evolution EL-P", "all", 4100),
    ("Tibhar", "Evolution MX-D", "off", 4200), ("Tibhar", "Grass D.TecS", "def", 2500),
    ("Joola", "Rhyzm", "off", 3500), ("Joola", "Rhyzm-P", "off", 3600),
    ("Joola", "Dynaryz AGR", "off", 3700), ("Joola", "Dynaryz ZGR", "all", 3700),
    ("Stiga", "DNA Pro S", "off", 3800), ("Stiga", "DNA Pro M", "off", 3800),
    ("Stiga", "DNA Pro H", "off", 3900), ("Stiga", "DNA Platinum S", "off", 4300),
    ("Stiga", "DNA Platinum M", "off", 4300), ("Stiga", "DNA Platinum H", "off", 4400),
]
SPONGES = ["1.8mm", "2.0mm", "2.1mm", "2.2mm", "MAX"]

# (brand, product, price of the 25ml bottle)
GLUE_BASES = [
    ("Butterfly", "Free Chack", 300), ("Butterfly", "Free Chack II", 350),
    ("Yasaka", "Free Glue", 280), ("Donic", "Aqua Glue", 300),
    ("Andro", "Water Glue", 320), ("Tibhar", "Fix Glue", 330),
    ("Joola", "Fix n Go", 350), ("Stiga", "Free Glue", 290),
    ("Nittaku", "Water Based Glue", 340), ("DHS", "Water Glue", 220),
    ("Xiom", "Water Glue", 300), ("729", "Friendship Glue", 180),
    ("Palio", "Free Glue", 260), ("Killerspin", "Quick Glue", 400),
]
GLUE_SIZES = [("25ml", 1.0, 3), ("50ml", 1.7, 5), ("100ml", 3.0, 2)]   # (label, price multiplier, popularity weight)

STYLE_TAG = {"offensive": "off", "all_round": "all", "defensive": "def"}


def esc(v):
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def write_batches(f, table, cols, rows):
    col_sql = ", ".join(cols)
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i + BATCH]
        vals = ",\n".join("(" + ", ".join(r) + ")" for r in chunk)
        f.write(f"INSERT INTO {table} ({col_sql}) VALUES\n{vals};\n\n")


# ------------------------------------------------------------
# PLAYER
# ------------------------------------------------------------
players = []
for pid in range(1, N_PLAYERS + 1):
    style = random.choices(["offensive", "all_round", "defensive"], weights=[45, 35, 20])[0]
    grip = random.choices(["shakehand", "penhold"], weights=[88, 12])[0]
    players.append({"id": pid, "name": fake.name(), "style": style, "grip": grip})

# ------------------------------------------------------------
# BLADE  (26 models x 5 handle types = 130)
# ------------------------------------------------------------
blades = []
bid = 1
for brand, model, material, plies, w, price, tag in BLADE_BASES:
    for handle, w_off in HANDLES.items():
        weight = round(w + w_off + random.uniform(-3, 3), 1)
        p = int(round((price + random.randint(-300, 300)) / 50.0) * 50)
        blades.append({"id": bid, "brand": brand, "model": f"{model} ({handle})",
                       "plies": plies, "weight": weight, "material": material,
                       "price": p, "tag": tag, "handle": handle})
        bid += 1

# ------------------------------------------------------------
# RUBBER  (67 models)
# ------------------------------------------------------------
rubbers = []
for rid, (brand, model, tag, price) in enumerate(RUBBER_BASES, start=1):
    rubbers.append({"id": rid, "brand": brand, "model": model,
                    "sponge": random.choice(SPONGES),
                    "price": int(round((price + random.randint(-150, 150)) / 50.0) * 50),
                    "tag": tag})

# ------------------------------------------------------------
# GLUE  (14 products x 3 sizes = 42)
# ------------------------------------------------------------
glues = []
gid = 1
for brand, product, base in GLUE_BASES:
    for label, mult, pop in GLUE_SIZES:
        glues.append({"id": gid, "name": f"{product} {label}", "brand": brand,
                      "price": int(round(base * mult / 10.0) * 10), "pop": pop})
        gid += 1

# ------------------------------------------------------------
# SETUP  - 1 setup per player minimum, rest spread randomly (<= 6 each)
# ------------------------------------------------------------
counts = {p["id"]: 1 for p in players}
extra = N_SETUPS - N_PLAYERS
while extra > 0:
    pid = random.randint(1, N_PLAYERS)
    if counts[pid] < 6:
        counts[pid] += 1
        extra -= 1

START, END = datetime(2019, 1, 1), datetime(2026, 8, 1)
span = int((END - START).total_seconds())


def weighted_pick(items, style, penhold=False, handle_pref=False):
    tag = STYLE_TAG[style]
    weights = []
    for it in items:
        w = 5 if it["tag"] == tag else 1
        if handle_pref:
            w *= 8 if (it["handle"] == "PEN") == penhold else 1
        weights.append(w)
    return random.choices(items, weights=weights)[0]


setups = []
sid = 1
for p in players:
    n = counts[p["id"]]
    stamps = set()
    while len(stamps) < n:                       # distinct timestamps per player
        stamps.add(START + timedelta(seconds=random.randint(0, span)))
    prev_blade = None
    for ts in sorted(stamps):
        if prev_blade and random.random() < 0.5:    # half the time the player keeps their blade
            blade = prev_blade
        else:
            blade = weighted_pick(blades, p["style"], penhold=(p["grip"] == "penhold"), handle_pref=True)
        prev_blade = blade
        fh = weighted_pick(rubbers, p["style"])
        bh = fh if random.random() < 0.3 else weighted_pick(rubbers, p["style"])
        glue = random.choices(glues, weights=[g["pop"] for g in glues])[0]
        setups.append({"id": sid, "player": p["id"], "ts": ts.strftime("%Y-%m-%d %H:%M:%S"),
                       "blade": blade["id"], "fh": fh["id"], "bh": bh["id"], "glue": glue["id"]})
        sid += 1

# ------------------------------------------------------------
# WRITE SQL
# ------------------------------------------------------------
with open(OUT_FILE, "w") as f:
    f.write("-- TTMS sample data (auto-generated by generate_ttms_data.py)\n")
    f.write("USE TTMS;\n\nSTART TRANSACTION;\n\n")

    write_batches(f, "Player", ["player_id", "name", "playing_style", "grip_type"],
                  [[str(p["id"]), esc(p["name"]), esc(p["style"]), esc(p["grip"])] for p in players])

    write_batches(f, "Blade", ["blade_id", "brand", "model", "ply_count", "weight_g", "material", "price"],
                  [[str(b["id"]), esc(b["brand"]), esc(b["model"]), str(b["plies"]),
                    str(b["weight"]), esc(b["material"]), str(b["price"])] for b in blades])

    write_batches(f, "Rubber", ["rubber_id", "brand", "model", "sponge", "price"],
                  [[str(r["id"]), esc(r["brand"]), esc(r["model"]), esc(r["sponge"]), str(r["price"])] for r in rubbers])

    write_batches(f, "Glue", ["glue_id", "name", "brand", "price"],
                  [[str(g["id"]), esc(g["name"]), esc(g["brand"]), str(g["price"])] for g in glues])

    write_batches(f, "Setup",
                  ["setup_id", "player_id", "created_at", "blade_id", "forehand_rubber_id", "backhand_rubber_id", "glue_id"],
                  [[str(s["id"]), str(s["player"]), esc(s["ts"]), str(s["blade"]),
                    str(s["fh"]), str(s["bh"]), str(s["glue"])] for s in setups])

    f.write("COMMIT;\n")

total = len(players) + len(blades) + len(rubbers) + len(glues) + len(setups)
print(f"Player: {len(players)}  Blade: {len(blades)}  Rubber: {len(rubbers)}  "
      f"Glue: {len(glues)}  Setup: {len(setups)}")
print(f"TOTAL RECORDS: {total}")