"""Game constants for zombie shooter."""

from __future__ import annotations

# Window
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Player
PLAYER_SPEED = 300  # pixels per second
PLAYER_RADIUS = 18
PLAYER_MAX_HP = 100
CONTACT_DPS = 10  # damage per second
PLAYER_ANIMATION_FPS = 10  # Frame rate for walk cycle animation
PLAYER_SPRITE_SIZE = 48  # Width/height of sprite in pixels
PLAYER_FRAME_COUNT = 3  # Number of frames per direction (walk cycle)
PLAYER_SHOOT_DURATION = 0.1  # Seconds to display shooting animation

# Bullets
BULLET_SPEED = 1800
BULLET_RADIUS = 4
BULLET_TTL = 1.5  # time to live in seconds
SHOOT_COOLDOWN = 0.15

# Acid Projectiles (Spitter variant)
ACID_PROJECTILE_SPEED = 300  # Slower than bullets (700)
ACID_PROJECTILE_RADIUS = 8  # Larger than bullets (4)
ACID_PROJECTILE_TTL = 2.5  # Longer lifetime than bullets (1.5)
ACID_PROJECTILE_DAMAGE = 5  # Damage per hit

# Spitter variant attack
SPITTER_ATTACK_COOLDOWN = 1.5  # Seconds between attacks
SPITTER_ATTACK_RANGE = 400  # Pixels - when to start attacking

# Exploder variant explosion
EXPLODER_EXPLOSION_RADIUS = 80  # Pixels - AOE damage radius
EXPLODER_EXPLOSION_DAMAGE_TO_ZOMBIES = 1  # HP damage per nearby zombie
EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER = 10  # HP damage if player in radius
EXPLODER_PARTICLE_COUNT = 16  # More particles than normal death (vs 8)
EXPLODER_PARTICLE_SPEED = 300  # Faster particles than blood (vs 150)
EXPLODER_PARTICLE_LIFETIME = 0.5  # Shorter for dramatic effect (vs 0.8)

# Weapons
WEAPON_STATS: dict[str, dict[str, float]] = {
    "pistol": {
        "fire_rate": 0.15,  # seconds between shots
        "bullet_count": 1,  # bullets per shot
        "spread_angle": 0.0,  # degrees spread for multi-shot
    },
    "shotgun": {
        "fire_rate": 0.5,  # slower fire rate
        "bullet_count": 5,  # 5 pellets per shot
        "spread_angle": 30.0,  # ±30° spread total
    },
    "smg": {
        "fire_rate": 0.08,  # rapid fire
        "bullet_count": 1,  # single bullet
        "spread_angle": 0.0,  # no spread
    },
}

# Pickups
PICKUP_SPAWN_RATE = 15.0  # seconds between pickup spawns
PICKUP_RADIUS = 20  # collision radius for pickups
PICKUP_TTL = 30.0  # time to live in seconds for pickups
PICKUP_SPAWN_MARGIN = 100  # pixels buffer from screen edge for safe spawn area

# Zombies
ZOMBIE_SPEED = 140
ZOMBIE_RADIUS = 16
MAX_ZOMBIES = 50
ZOMBIE_ANIMATION_FPS = 10  # Frame rate for walk cycle animation
ZOMBIE_SPRITE_SIZE = 48  # Width/height of sprite in pixels
ZOMBIE_FRAME_COUNT = 3  # Number of frames per direction (walk cycle)

# Zombie variants
ZOMBIE_VARIANTS: dict[str, dict[str, int | float]] = {
    "normal": {
        "speed": 140,
        "hp": 1,
        "radius": 16,
        "weight": 7,  # 70% spawn rate
    },
    "runner": {
        "speed": 280,  # 2x speed
        "hp": 1,
        "radius": 16,
        "weight": 1.5,  # 15% spawn rate
    },
    "tank": {
        "speed": 98,  # 0.7x speed
        "hp": 3,  # Requires 3 hits
        "radius": 24,  # Larger hitbox
        "weight": 1.5,  # 15% spawn rate (enabled in Phase 3)
    },
    "exploder": {
        "speed": 140,  # Normal speed
        "hp": 1,
        "radius": 16,
        "weight": 1.0,  # 10% spawn rate (enabled in Phase 4)
    },
    "spitter": {
        "speed": 100,  # Slow movement
        "hp": 1,
        "radius": 16,
        "weight": 1.0,  # 10% spawn rate (enabled in Phase 5)
    },
}

# Blood particles
BLOOD_PARTICLE_COUNT = 8  # Particles spawned per death
BLOOD_PARTICLE_SPEED = 150  # Initial velocity magnitude (pixels/sec)
BLOOD_PARTICLE_LIFETIME = 0.8  # Seconds before particle fades out
BLOOD_PARTICLE_RADIUS = 3  # Pixel radius of particle

# Gore effects
CORPSE_PERSISTENCE = 10.0  # Seconds dead zombie remains visible
BLOOD_POOL_SIZE = 28  # Pixel diameter of blood pool

# Spawning
SPAWN_INTERVAL_START = 1.0
SPAWN_INTERVAL_MIN = 0.25
SPAWN_RAMP_SECONDS = 45

# Win Condition
SURVIVE_SECONDS = 60

# ─── Ground Zones ─────────────────────────────────────────────────────────────
# Colors as plain RGB tuples (no pygame import in constants.py)
GROUND_GRASS_COLOR: tuple[int, int, int] = (42, 58, 32)
GROUND_DIRT_COLOR: tuple[int, int, int] = (72, 57, 38)
GROUND_ASPHALT_COLOR: tuple[int, int, int] = (36, 36, 36)
GROUND_ASPHALT_EDGE_COLOR: tuple[int, int, int] = (50, 50, 50)

# Ground geometry as (x, y, w, h) tuples — convert to pygame.Rect in play.py
GROUND_PATH_H: tuple[int, int, int, int] = (0, 310, 1280, 100)
GROUND_PATH_V: tuple[int, int, int, int] = (590, 0, 100, 720)
GROUND_PATH_SEAMS: list[tuple[int, int, int, int]] = [
    (0, 308, 1280, 4),
    (0, 408, 1280, 4),
    (588, 0, 4, 720),
    (688, 0, 4, 720),
]
GROUND_DIRT_RECTS: list[tuple[int, int, int, int]] = [
    (30, 30, 250, 170),
    (880, 40, 280, 150),
    (30, 480, 220, 200),
    (950, 460, 250, 220),
    (350, 30, 180, 120),
    (730, 430, 160, 140),
]

# ─── Obstacle Definitions ─────────────────────────────────────────────────────
# Each entry: (type, shape, cx, cy, w_or_r, h_or_r, base_color, flicker)
#   type:      "house" | "tree" | "car" | "pond" | "barrel"
#   shape:     "rect" | "circle" | "ellipse"
#   cx, cy:    center position
#   w_or_r:    width (rect/ellipse) OR radius (circle) — stored as half-width
#   h_or_r:    height (rect/ellipse) OR radius (circle, same value)
#   base_color: RGB tuple — each instance gets ±15 random offset at build time
#   flicker:   True for burning barrels
ObstacleDef = tuple[str, str, int, int, int, int, tuple[int, int, int], bool]

OBSTACLE_DEFS: list[ObstacleDef] = [
    # ── Houses (corners, large rects) ──────────────────────────────────────────
    # Top-left at y=45 (rect bottom=75) to stay clear of test zombies at y=100
    ("house", "rect",    75,  45, 100, 60, (55, 45, 38), False),
    ("house", "rect",  1175,  80, 110, 90, (48, 40, 34), False),
    ("house", "rect",   105, 640, 110, 90, (52, 43, 36), False),
    ("house", "rect",  1175, 640, 110, 90, (50, 42, 35), False),
    # ── Trees (circles, grass zones only) ──────────────────────────────────────
    # Top-left tree moved to y=60 so it's >30px from y=100 test zombies
    ("tree", "circle",  220,  60,  14, 14, (28, 52, 22), False),
    ("tree", "circle",  310, 185,  16, 16, (32, 58, 25), False),
    ("tree", "circle",  130, 230,  13, 13, (25, 48, 20), False),
    ("tree", "circle",  800, 110,  15, 15, (30, 54, 23), False),
    ("tree", "circle",  970, 190,  14, 14, (27, 50, 21), False),
    ("tree", "circle", 1120, 160,  16, 16, (33, 58, 26), False),
    ("tree", "circle",  175, 540,  15, 15, (29, 53, 22), False),
    ("tree", "circle",  320, 600,  13, 13, (26, 49, 20), False),
    ("tree", "circle",  840, 510,  16, 16, (31, 55, 24), False),
    ("tree", "circle", 1080, 595,  14, 14, (28, 51, 21), False),
    ("tree", "circle", 1170, 510,  15, 15, (30, 54, 23), False),
    # ── Crashed Cars (rects, on/near path) ─────────────────────────────────────
    ("car", "rect",   330, 358,  52, 26, (58, 52, 48), False),
    ("car", "rect",   430, 362,  50, 24, (62, 44, 38), False),
    ("car", "rect",   870, 355,  50, 26, (55, 50, 45), False),
    ("car", "rect",   638, 200,  26, 50, (60, 48, 40), False),
    ("car", "rect",   642, 570,  26, 50, (56, 44, 36), False),
    # ── Ponds (ellipses, grass zones) ──────────────────────────────────────────
    ("pond", "ellipse",  270, 490,  80, 54, (28, 45, 52), False),
    ("pond", "ellipse",  940, 155,  90, 58, (25, 42, 50), False),
    # ── Barrels (circles, near houses) — kept above y=80 to clear test zone ───
    ("barrel", "circle",  145,  65, 10, 10, (90, 55, 20), False),
    ("barrel", "circle",  175,  78, 10, 10, (85, 50, 18),  True),
    ("barrel", "circle", 1150,  95, 10, 10, (88, 52, 19), False),
    ("barrel", "circle", 1175, 130, 10, 10, (82, 48, 17),  True),
    ("barrel", "circle",  168, 595, 10, 10, (86, 51, 18), False),
    ("barrel", "circle", 1155, 595, 10, 10, (89, 54, 20),  True),
]

# ─── HUD ─────────────────────────────────────────────────────────────────────
HUD_PANEL_W = 440          # Width of bottom HUD panel in pixels
HUD_PANEL_H = 88           # Height of bottom HUD panel in pixels
HUD_FACE_SIZE = 60         # Face portrait diameter in pixels
HUD_ICON_W = 52            # Weapon icon width in pixels
HUD_ICON_H = 30            # Weapon icon height in pixels
HUD_PAIN_FLASH_DURATION = 0.4  # Seconds pain flash face lasts after hit
