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
BULLET_SPEED = 700
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
