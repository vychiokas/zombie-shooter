"""Play scene for zombie shooter."""

from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

import pygame

from game.core.constants import (
    BLOOD_PARTICLE_COUNT,
    BLOOD_PARTICLE_SPEED,
    CONTACT_DPS,
    EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER,
    EXPLODER_EXPLOSION_DAMAGE_TO_ZOMBIES,
    EXPLODER_EXPLOSION_RADIUS,
    EXPLODER_PARTICLE_COUNT,
    EXPLODER_PARTICLE_SPEED,
    GROUND_ASPHALT_EDGE_COLOR,
    GROUND_DIRT_RECTS,
    GROUND_PATH_H,
    GROUND_PATH_SEAMS,
    GROUND_PATH_V,
    HEIGHT,
    HUD_FACE_SIZE,
    HUD_ICON_H,
    HUD_ICON_W,
    HUD_PANEL_H,
    HUD_PANEL_W,
    MAX_ZOMBIES,
    PICKUP_SPAWN_MARGIN,
    PICKUP_SPAWN_RATE,
    WEAPON_STATS,
    WIDTH,
)
from game.core.scene import Scene
from game.entities.acid_projectile import AcidProjectile
from game.entities.blood_decal import BloodDecal
from game.entities.blood_particle import BloodParticle
from game.entities.bullet import Bullet
from game.entities.dead_zombie import DeadZombie
from game.entities.obstacle import Obstacle, build_obstacles
from game.entities.pickup import Pickup
from game.entities.player import Player
from game.entities.zombie import Zombie
from game.systems.collisions import (
    check_acid_projectile_player_collisions,
    check_bullet_zombie_collisions,
    check_collision_circle,
    check_player_pickup_collisions,
    check_player_zombie_collisions,
)
from game.systems.spawner import ZombieSpawner
from game.systems.weapon_art import build_weapon_icons

if TYPE_CHECKING:
    from game.core.game import Game


_TILE_SIZE = 16  # pixel art tile size


def _make_grass_tile() -> pygame.Surface:
    """Generate a 16×16 pixel art grass tile with blade detail."""
    import random as _r

    rng = _r.Random(0xBEEF_CAFE)
    tile = pygame.Surface((_TILE_SIZE, _TILE_SIZE))
    tile.fill((38, 52, 28))
    # Scatter light/dark speckles
    for _ in range(28):
        x, y = rng.randint(0, 15), rng.randint(0, 15)
        tile.set_at((x, y), (55, 76, 40) if rng.random() > 0.45 else (24, 36, 16))
    # Grass blade hints: short 2-px vertical strokes
    for _ in range(6):
        x, y = rng.randint(1, 14), rng.randint(3, 13)
        tile.set_at((x, y), (68, 92, 50))
        tile.set_at((x, y - 1), (50, 70, 36))
    return tile


def _make_dirt_tile() -> pygame.Surface:
    """Generate a 16×16 pixel art dirt tile with pebble detail."""
    import random as _r

    rng = _r.Random(0xDEAD_BEEF)
    tile = pygame.Surface((_TILE_SIZE, _TILE_SIZE))
    tile.fill((65, 50, 33))
    # Light/dark speckles
    for _ in range(22):
        x, y = rng.randint(0, 15), rng.randint(0, 15)
        tile.set_at((x, y), (82, 65, 44) if rng.random() > 0.5 else (48, 36, 22))
    # Small pebble clusters (2×2)
    for _ in range(4):
        px, py = rng.randint(1, 13), rng.randint(1, 13)
        c = (76, 60, 40)
        for dx in range(2):
            for dy in range(2):
                tile.set_at((px + dx, py + dy), c)
    return tile


def _make_asphalt_tile() -> pygame.Surface:
    """Generate a 16×16 pixel art asphalt tile with gravel/crack detail."""
    import random as _r

    rng = _r.Random(0xC0FFEE_42)
    tile = pygame.Surface((_TILE_SIZE, _TILE_SIZE))
    tile.fill((30, 30, 30))
    # Subtle light speckle (gravel)
    for _ in range(12):
        x, y = rng.randint(0, 15), rng.randint(0, 15)
        v = rng.randint(42, 52)
        tile.set_at((x, y), (v, v, v))
    # Rare darker crack pixels
    for _ in range(3):
        x, y = rng.randint(0, 15), rng.randint(0, 15)
        tile.set_at((x, y), (20, 20, 20))
        if rng.random() > 0.5 and x < 15:
            tile.set_at((x + 1, y), (22, 22, 22))
    return tile


def _tile_region(
    surface: pygame.Surface,
    tile: pygame.Surface,
    region: pygame.Rect,
) -> None:
    """Tile a pixel-art tile across a rectangular region of surface."""
    for ty in range(region.top, region.bottom, _TILE_SIZE):
        for tx in range(region.left, region.right, _TILE_SIZE):
            surface.blit(tile, (tx, ty))


def _build_ground_surface() -> pygame.Surface:
    """Build pre-baked ground terrain surface with pixel-art tile textures.

    Paints terrain zones using tiled 16×16 pixel-art surfaces:
    1. Grass tiles across entire screen
    2. Dirt patch tiles over grass zones
    3. Asphalt tiles for cross-shaped path
    4. Path edge seam lines

    Returns:
        Pygame Surface with pixel-art terrain baked in; blit each frame O(1).
    """
    surface = pygame.Surface((WIDTH, HEIGHT))

    grass_tile = _make_grass_tile()
    dirt_tile = _make_dirt_tile()
    asphalt_tile = _make_asphalt_tile()

    # 1. Tile grass across entire surface
    _tile_region(surface, grass_tile, pygame.Rect(0, 0, WIDTH, HEIGHT))

    # 2. Tile dirt patches over grass
    for x, y, w, h in GROUND_DIRT_RECTS:
        _tile_region(surface, dirt_tile, pygame.Rect(x, y, w, h))

    # 3. Tile asphalt paths (horizontal + vertical)
    hx, hy, hw, hh = GROUND_PATH_H
    vx, vy, vw, vh = GROUND_PATH_V
    _tile_region(surface, asphalt_tile, pygame.Rect(hx, hy, hw, hh))
    _tile_region(surface, asphalt_tile, pygame.Rect(vx, vy, vw, vh))

    # 4. Path edge seams (thin pixel line for asphalt kerb)
    for x, y, w, h in GROUND_PATH_SEAMS:
        pygame.draw.rect(surface, GROUND_ASPHALT_EDGE_COLOR, pygame.Rect(x, y, w, h))

    return surface


# ─── HUD helpers ──────────────────────────────────────────────────────────────

_WEAPON_ORDER: tuple[str, ...] = ("pistol", "shotgun", "smg")


def _get_face_state(hp: float, pain_timer: float) -> str:
    """Return face expression state string based on HP and pain timer.

    Args:
        hp: Current player HP (0-100).
        pain_timer: Seconds remaining in pain flash (0 = no flash).

    Returns:
        One of: "pain_flash", "normal", "hurt", "injured", "critical", "dying".
    """
    if pain_timer > 0:
        return "pain_flash"
    if hp >= 80:
        return "normal"
    if hp >= 60:
        return "hurt"
    if hp >= 40:
        return "injured"
    if hp >= 20:
        return "critical"
    return "dying"


def _draw_rambo_mouth(
    screen: pygame.Surface,
    cx: int,
    my: int,
    r: int,
    state: str,
) -> None:
    """Draw mouth/teeth appropriate for the given state.

    Args:
        screen: Surface to draw on.
        cx: Face center x.
        my: Mouth center y.
        r: Face radius.
        state: Expression state string.
    """
    tw = r * 2 // 3          # tooth strip width
    dark = (45, 25, 12)
    teeth = (240, 228, 210)

    if state == "normal":
        # Big wide confident grin — teeth clearly visible
        th = max(5, r // 5)
        trect = pygame.Rect(cx - tw // 2, my - th // 2, tw, th)
        pygame.draw.rect(screen, teeth, trect)
        # Tooth dividers
        for dx in (0, -tw // 4, tw // 4):
            pygame.draw.line(
                screen, dark,
                (cx + dx, my - th // 2), (cx + dx, my + th // 2), 1,
            )
        # Smile outline
        pygame.draw.rect(screen, dark, trect, 2)
        # Upturned corner lines
        pygame.draw.line(
            screen, dark,
            (cx - tw // 2, my - 1), (cx - tw // 2 - 4, my - 4), 2,
        )
        pygame.draw.line(
            screen, dark,
            (cx + tw // 2, my - 1), (cx + tw // 2 + 4, my - 4), 2,
        )

    elif state in ("hurt", "pain_flash"):
        # Tight grimace — narrow slit, teeth barely showing
        th = max(3, r // 7)
        trect = pygame.Rect(cx - tw * 2 // 5, my - th // 2, tw * 4 // 5, th)
        pygame.draw.rect(screen, teeth, trect)
        pygame.draw.rect(screen, dark, trect, 1)
        # Slight downward corner pull
        pygame.draw.line(
            screen, dark,
            (trect.left, my), (trect.left - 2, my + 2), 2,
        )
        pygame.draw.line(
            screen, dark,
            (trect.right, my), (trect.right + 2, my + 2), 2,
        )

    else:
        # Clenched grimace — teeth visible, corners pulled down
        th = max(4, r // 6)
        trect = pygame.Rect(cx - tw // 2, my - th // 2, tw, th)
        pygame.draw.rect(screen, teeth, trect)
        pygame.draw.rect(screen, dark, trect, 2)
        # Thick upper lip line
        pygame.draw.line(
            screen, (80, 35, 18),
            (trect.left, trect.top), (trect.right, trect.top), 2,
        )
        # Downturned corners
        pygame.draw.line(
            screen, dark,
            (trect.left, my), (trect.left - 4, my + th // 2 + 1), 2,
        )
        pygame.draw.line(
            screen, dark,
            (trect.right, my), (trect.right + 4, my + th // 2 + 1), 2,
        )


def _draw_hud_face(
    screen: pygame.Surface,
    cx: int,
    cy: int,
    r: int,
    state: str,
    look: str = "center",
    blink: bool = False,
) -> None:
    """Draw Rambo-style procedural face portrait at (cx, cy) with radius r.

    Features: red headband, olive skin, strong brows, progressive nose bleed.
    Idle animations driven by ``look`` (pupil offset) and ``blink`` (closed lid).

    Args:
        screen: Surface to draw on.
        cx: Center x coordinate.
        cy: Center y coordinate.
        r: Face radius in pixels (half of HUD_FACE_SIZE).
        state: Expression state from _get_face_state().
        look: Gaze direction — "left", "center", or "right".
        blink: If True, draw eyelids closed instead of open eyes.
    """
    # Olive/tan skin — pales with damage
    skin: tuple[int, int, int] = {
        "pain_flash": (210, 158, 100),
        "normal":     (200, 152,  92),
        "hurt":       (188, 142,  82),
        "injured":    (175, 130,  70),
        "critical":   (158, 116,  58),
        "dying":      (135,  98,  46),
    }[state]
    outline = (max(0, skin[0] - 45), max(0, skin[1] - 42), max(0, skin[2] - 35))

    # ── Head ─────────────────────────────────────────────────────────────────
    pygame.draw.circle(screen, skin, (cx, cy), r)

    # Red headband across forehead (rect; corners outside circle blend into
    # the dark HUD panel background)
    band_h = max(6, r // 4)
    band_y = cy - r + 2
    pygame.draw.rect(
        screen, (148, 22, 22),
        pygame.Rect(cx - r, band_y, r * 2, band_h),
    )
    # Lighter centre stripe on headband
    pygame.draw.line(
        screen, (195, 45, 45),
        (cx - r, band_y + band_h // 2),
        (cx + r, band_y + band_h // 2),
        2,
    )
    # Re-draw circle outline to visually contain the headband
    pygame.draw.circle(screen, outline, (cx, cy), r, 2)

    # ── Geometry ─────────────────────────────────────────────────────────────
    ex_l = cx - r // 3
    ex_r = cx + r // 3
    ey   = cy - r // 5
    er   = max(3, r // 5)
    ny   = cy + er // 2          # nose-tip y
    my   = cy + r * 3 // 8      # mouth y

    # ── Strong angled brows (always drawn, give intensity) ────────────────────
    brow = (38, 26, 14)
    pygame.draw.line(screen, brow, (ex_l - er, ey - er), (ex_l + er, ey - er + 3), 3)
    pygame.draw.line(screen, brow, (ex_r - er, ey - er + 3), (ex_r + er, ey - er), 3)

    # ── Nostril dots (always drawn) ────────────────────────────────────────────
    pygame.draw.circle(screen, outline, (cx - 3, ny), 2)
    pygame.draw.circle(screen, outline, (cx + 3, ny), 2)

    # ── State-specific eyes, blood, and mouth ─────────────────────────────────
    # Pupil x-offset for look direction (applied only in open-eye states)
    pdx = {"left": -max(1, er // 3), "right": max(1, er // 3), "center": 0}[look]

    if state == "pain_flash":
        # Eyes snapped shut hard — thick lines (ignores look/blink)
        for ex in (ex_l, ex_r):
            pygame.draw.line(screen, brow, (ex - er, ey), (ex + er, ey), 4)
        # Slight nose-blood smear
        pygame.draw.line(screen, (195, 18, 18), (cx - 1, ny + 2), (cx - 1, my - 4), 2)
        _draw_rambo_mouth(screen, cx, my, r, state)

    elif state == "normal":
        if blink:
            # Eyelids closed — whites visible, skin-coloured lid line
            for ex in (ex_l, ex_r):
                pygame.draw.circle(screen, (255, 255, 240), (ex, ey), er)
                pygame.draw.line(screen, skin, (ex - er, ey), (ex + er, ey), 3)
        else:
            # Open eyes — pupil shifted by look direction
            for ex in (ex_l, ex_r):
                pygame.draw.circle(screen, (255, 255, 240), (ex, ey), er)
                pygame.draw.circle(screen, (42, 28, 14), (ex + pdx, ey), er // 2 + 1)
                pygame.draw.circle(
                    screen, (255, 255, 255),
                    (ex + pdx - 1, ey - 1), max(1, er // 4),
                )
        _draw_rambo_mouth(screen, cx, my, r, state)

    elif state == "hurt":
        if blink:
            for ex in (ex_l, ex_r):
                pygame.draw.circle(screen, (255, 255, 240), (ex, ey), er)
                pygame.draw.line(screen, skin, (ex - er, ey), (ex + er, ey), er + 1)
        else:
            # Eyes narrowed with squint — pupil shifted by look direction
            for ex in (ex_l, ex_r):
                pygame.draw.circle(screen, (255, 255, 240), (ex, ey), er)
                pygame.draw.circle(screen, (42, 28, 14), (ex + pdx, ey), er // 2 + 1)
                pygame.draw.line(screen, skin, (ex - er, ey - 2), (ex + er, ey - 2), 3)
        # Small blood drop below nose
        pygame.draw.circle(screen, (200, 18, 18), (cx, ny + 5), 2)
        _draw_rambo_mouth(screen, cx, my, r, state)

    elif state == "injured":
        # Left eye bruised (dark ring), right squinting hard
        pygame.draw.circle(screen, (85, 28, 18), (ex_l, ey), er + 2)
        pygame.draw.circle(screen, (255, 215, 190), (ex_l, ey), er)
        pygame.draw.circle(screen, (42, 28, 14), (ex_l, ey), er // 2)
        pygame.draw.line(screen, skin, (ex_l - er, ey - 2), (ex_l + er, ey - 2), 4)
        pygame.draw.circle(screen, (255, 248, 230), (ex_r, ey), er)
        pygame.draw.circle(screen, (42, 28, 14), (ex_r, ey), er // 2 + 1)
        pygame.draw.line(screen, skin, (ex_r - er, ey - 2), (ex_r + er, ey - 2), 3)
        # Blood dripping from nose
        pygame.draw.line(
            screen, (200, 18, 18), (cx - 1, ny + 2), (cx - 1, my - 3), 2
        )
        pygame.draw.circle(screen, (200, 18, 18), (cx - 1, my - 2), 2)
        _draw_rambo_mouth(screen, cx, my, r, state)

    elif state == "critical":
        # Both eyes bruised and swollen
        for ex in (ex_l, ex_r):
            pygame.draw.circle(screen, (95, 22, 14), (ex, ey), er + 2)
            pygame.draw.circle(screen, (255, 195, 170), (ex, ey), er)
            pygame.draw.circle(screen, (42, 28, 14), (ex, ey), er // 2)
            pygame.draw.line(screen, skin, (ex - er, ey - 2), (ex + er, ey - 2), 5)
        # Heavy nose bleed streaming down
        pygame.draw.line(
            screen, (190, 14, 14), (cx - 1, ny + 1), (cx - 1, my + 1), 3
        )
        pygame.draw.line(
            screen, (165, 10, 10), (cx + 2, ny + 3), (cx + 2, my - 1), 2
        )
        # Blood pooling at chin
        pygame.draw.circle(screen, (178, 12, 12), (cx, my + 4), 3)
        _draw_rambo_mouth(screen, cx, my, r, state)

    else:  # dying
        # Eyes barely open — thick drooping lids
        for ex in (ex_l, ex_r):
            pygame.draw.circle(screen, (105, 28, 14), (ex, ey), er + 2)
            pygame.draw.circle(screen, (220, 168, 145), (ex, ey), er)
            pygame.draw.circle(screen, (48, 30, 18), (ex, ey), er // 2)
            pygame.draw.line(screen, skin, (ex - er, ey - 1), (ex + er, ey - 1), er + 2)
        # Blood everywhere
        pygame.draw.line(
            screen, (178, 10, 10), (cx - 2, ny), (cx - 2, cy + r - 5), 3
        )
        pygame.draw.line(
            screen, (155, 8, 8), (cx + 2, ny + 2), (cx + 2, my + 3), 2
        )
        pygame.draw.circle(screen, (172, 10, 10), (cx, my + 6), 4)
        _draw_rambo_mouth(screen, cx, my, r, state)




def _draw_weapon_icons(
    screen: pygame.Surface,
    panel_x: int,
    panel_y: int,
    icons: dict[str, pygame.Surface],
    inventory: set[str],
    current: str,
) -> None:
    """Draw weapon icon slots on the HUD panel.

    Args:
        screen: Surface to draw on.
        panel_x: Left edge of the icons area.
        panel_y: Top edge of the icons area.
        icons: Pre-built icon surfaces from _build_weapon_icons().
        inventory: Set of owned weapon names.
        current: Currently equipped weapon name.
    """
    slot_pad = 6

    for i, weapon in enumerate(_WEAPON_ORDER):
        sx = panel_x + i * (HUD_ICON_W + slot_pad)
        sy = panel_y
        slot_rect = pygame.Rect(sx, sy, HUD_ICON_W, HUD_ICON_H)
        owned = weapon in inventory
        active = weapon == current

        bg = (55, 48, 32) if active else ((35, 32, 28) if owned else (22, 20, 18))
        pygame.draw.rect(screen, bg, slot_rect)

        border = (220, 190, 40) if active else (55, 52, 48)
        pygame.draw.rect(screen, border, slot_rect, 2 if active else 1)

        icon = icons.get(weapon)
        if icon is None:
            continue
        tinted = icon.copy()
        if not owned:
            tinted.fill((60, 60, 60, 0), special_flags=pygame.BLEND_RGB_MULT)
        elif active:
            tinted.fill((255, 240, 180, 0), special_flags=pygame.BLEND_RGB_MULT)
        screen.blit(tinted, slot_rect)


class PlayScene(Scene):
    """Main gameplay scene."""

    def __init__(self, game: Game) -> None:
        """Initialize play scene.

        Args:
            game: Game instance for scene switching.
        """
        self.game = game
        self.player = Player(pygame.Vector2(WIDTH / 2, HEIGHT / 2))
        self.bullets: list[Bullet] = []
        self.zombies: list[Zombie] = []
        self.pickups: list[Pickup] = []
        self.blood_particles: list[BloodParticle] = []
        self.dead_zombies: list[DeadZombie] = []
        self.blood_decals: list[BloodDecal] = []
        self.acid_projectiles: list[AcidProjectile] = []
        self.spawner = ZombieSpawner()
        self.timer = 0.0
        self.pickup_spawn_timer = 0.0
        self.kills = 0
        self.font = pygame.font.Font(None, 36)
        # Pre-baked terrain surface (drawn once, blitted every frame)
        self._ground = _build_ground_surface()
        # Fixed obstacle layout (built once per session)
        self._obstacles: list[Obstacle] = build_obstacles()
        # Pre-built weapon icon surfaces for HUD (built once)
        self._weapon_icons: dict[str, pygame.Surface] = build_weapon_icons()
        # Face idle-animation state (look-around + blink)
        self._face_look: str = "center"
        self._face_look_timer: float = random.uniform(4.0, 8.0)
        self._face_blink_timer: float = 0.0
        self._face_blink_cooldown: float = random.uniform(2.0, 5.0)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle play scene events.

        Args:
            event: Pygame event to process.
        """
        # Weapon switching with number keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.player.switch_weapon("pistol")
            elif event.key == pygame.K_2:
                self.player.switch_weapon("shotgun")
            elif event.key == pygame.K_3:
                self.player.switch_weapon("smg")

    def spawn_blood_splash(self, pos: pygame.Vector2) -> None:
        """Spawn blood particles at position with random outward velocities.

        Args:
            pos: Position to spawn particles from.
        """
        for _ in range(BLOOD_PARTICLE_COUNT):
            # Random angle (0 to 2π)
            angle = random.uniform(0, 2 * math.pi)
            # Random speed variation (75% to 125% of base speed)
            speed = BLOOD_PARTICLE_SPEED * random.uniform(0.75, 1.25)

            # Convert angle to velocity vector
            vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)

            self.blood_particles.append(BloodParticle(pos, vel))

    def apply_explosion(self, explosion_pos: pygame.Vector2) -> None:
        """Apply AOE explosion damage to player and zombies.

        Handles:
        1. Damage to player if within radius (10 HP)
        2. Damage to nearby zombies (1 HP each)
        3. Chain reaction handling (newly killed Exploders trigger recursively)
        4. Enhanced particle effect (more/faster than normal death)

        Args:
            explosion_pos: Center of explosion (dead Exploder position).
        """
        # Damage player if within radius
        if check_collision_circle(
            explosion_pos,
            EXPLODER_EXPLOSION_RADIUS,
            self.player.pos,
            self.player.radius,
        ):
            self.player.take_damage(EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER)

        # Damage nearby zombies (potential chain reactions)
        newly_dead_exploders = []
        for zombie in self.zombies:
            if check_collision_circle(
                explosion_pos,
                EXPLODER_EXPLOSION_RADIUS,
                zombie.pos,
                zombie.radius,
            ):
                initial_hp = zombie.hp
                zombie.hp -= EXPLODER_EXPLOSION_DAMAGE_TO_ZOMBIES

                # Check if zombie JUST died from THIS explosion (was alive, now dead)
                if initial_hp > 0 and zombie.hp <= 0 and zombie.variant == "exploder":
                    newly_dead_exploders.append(zombie.pos.copy())

        # Spawn enhanced explosion particle effect
        for _ in range(EXPLODER_PARTICLE_COUNT):
            angle = random.uniform(0, 2 * math.pi)
            speed = EXPLODER_PARTICLE_SPEED * random.uniform(0.75, 1.25)
            vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            self.blood_particles.append(BloodParticle(explosion_pos, vel))

        # Chain reaction: recursively explode newly killed Exploders
        for exploder_pos in newly_dead_exploders:
            self.apply_explosion(exploder_pos)

    def _handle_shooting(self) -> None:
        """Poll mouse and fire bullets if left button is held."""
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left mouse button held
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            bullets = self.player.shoot(mouse_pos)
            self.bullets.extend(bullets)

    def _update_entities(self, dt: float) -> None:
        """Advance bullets, particles, corpses, decals, and acid projectiles.

        Args:
            dt: Delta time in seconds.
        """
        self.bullets = [b for b in self.bullets if b.update(dt)]
        self.blood_particles = [p for p in self.blood_particles if p.update(dt)]
        self.dead_zombies = [z for z in self.dead_zombies if z.update(dt)]
        self.blood_decals = [d for d in self.blood_decals if d.update(dt)]
        self.acid_projectiles = [p for p in self.acid_projectiles if p.update(dt)]

    def _handle_zombie_spawning(self, dt: float) -> None:
        """Spawn zombies via the spawner and update all living zombies.

        Also collects pending acid projectiles from spitter zombies.

        Args:
            dt: Delta time in seconds.
        """
        if self.spawner.update(dt, self.timer) and len(self.zombies) < MAX_ZOMBIES:
            spawn_pos = self.spawner.get_spawn_position()
            variant = self.spawner.get_spawn_variant()
            self.zombies.append(Zombie(spawn_pos, variant))

        for zombie in self.zombies:
            zombie.update(dt, self.player.pos, self._obstacles)
            if zombie.variant == "spitter" and zombie.pending_projectiles:
                for pos, direction in zombie.pending_projectiles:
                    self.acid_projectiles.append(AcidProjectile(pos, direction))
                zombie.pending_projectiles.clear()

    def _handle_pickups(self, dt: float) -> None:
        """Advance pickup timer, spawn new pickup, update pickups, handle collection.

        Args:
            dt: Delta time in seconds.
        """
        self.pickup_spawn_timer += dt
        if self.pickup_spawn_timer >= PICKUP_SPAWN_RATE:
            self.pickup_spawn_timer = 0.0
            x = random.uniform(PICKUP_SPAWN_MARGIN, WIDTH - PICKUP_SPAWN_MARGIN)
            y = random.uniform(PICKUP_SPAWN_MARGIN, HEIGHT - PICKUP_SPAWN_MARGIN)
            spawn_pos = pygame.Vector2(x, y)
            weapon_type = random.choice(list(WEAPON_STATS.keys()))
            self.pickups.append(Pickup(spawn_pos, weapon_type))

        self.pickups = [p for p in self.pickups if p.update(dt)]

        colliding_pickups = check_player_pickup_collisions(
            self.player.pos, self.player.radius, self.pickups
        )
        if colliding_pickups:
            pickup_idx = colliding_pickups[0]
            pickup = self.pickups[pickup_idx]
            self.player.add_weapon(pickup.weapon_type)
            self.player.current_weapon = pickup.weapon_type
            self.pickups = [p for i, p in enumerate(self.pickups) if i != pickup_idx]

    def _process_bullet_hits(self) -> None:
        """Handle bullet-zombie collisions: damage, death effects, kill count."""
        bullet_zombie_hits = check_bullet_zombie_collisions(self.bullets, self.zombies)

        bullets_to_remove: set[int] = set()
        zombies_to_remove: set[int] = set()
        for b_idx, z_idx in bullet_zombie_hits:
            zombie = self.zombies[z_idx]
            zombie.hp -= 1
            bullets_to_remove.add(b_idx)

            if zombie.hp <= 0:
                if zombie.variant == "exploder":
                    self.apply_explosion(zombie.pos)

                self.spawn_blood_splash(zombie.pos)
                self.blood_decals.append(BloodDecal(zombie.pos))
                self.dead_zombies.append(DeadZombie(zombie.pos))
                zombies_to_remove.add(z_idx)
                self.kills += 1

        self.bullets = [
            b for i, b in enumerate(self.bullets) if i not in bullets_to_remove
        ]
        self.zombies = [
            z for i, z in enumerate(self.zombies) if i not in zombies_to_remove
        ]

    def _process_player_damage(self, dt: float) -> None:
        """Apply contact DPS from zombies and damage from acid projectile hits.

        Args:
            dt: Delta time in seconds.
        """
        colliding_zombies = check_player_zombie_collisions(
            self.player.pos, self.player.radius, self.zombies
        )
        if colliding_zombies:
            self.player.take_damage(CONTACT_DPS * dt * len(colliding_zombies))

        acid_hits = check_acid_projectile_player_collisions(
            self.player.pos, self.player.radius, self.acid_projectiles
        )
        projectiles_to_remove: set[int] = set()
        for p_idx in acid_hits:
            projectile = self.acid_projectiles[p_idx]
            self.player.take_damage(projectile.damage)
            projectiles_to_remove.add(p_idx)

        self.acid_projectiles = [
            p
            for i, p in enumerate(self.acid_projectiles)
            if i not in projectiles_to_remove
        ]

    def _check_game_over(self) -> None:
        """Transition to GameOverScene if player HP is depleted."""
        if self.player.hp <= 0:
            from game.scenes.game_over import GameOverScene

            self.game.change_scene(GameOverScene(self.game, self.kills, won=False))

    def update(self, dt: float) -> None:
        """Update gameplay.

        Args:
            dt: Delta time in seconds.
        """
        self.timer += dt
        self.player.update(dt, self._obstacles)
        self._handle_shooting()
        self._update_entities(dt)
        self._handle_zombie_spawning(dt)
        self._handle_pickups(dt)
        self._process_bullet_hits()
        self._process_player_damage(dt)
        self._check_game_over()

    def _draw_hud(self, screen: pygame.Surface) -> None:
        """Draw heads-up display: top text overlays + Doom-style bottom panel.

        Args:
            screen: Pygame surface to draw on.
        """
        # ── Top overlays ──────────────────────────────────────────────────────
        # Survival timer (top-center)
        timer_text = self.font.render(
            f"Survived: {self.timer:.1f}s", True, (255, 255, 255)
        )
        timer_rect = timer_text.get_rect(center=(WIDTH // 2, 25))
        screen.blit(timer_text, timer_rect)

        # Kills (top-right)
        kills_text = self.font.render(f"Kills: {self.kills}", True, (255, 255, 255))
        kills_rect = kills_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(kills_text, kills_rect)

        # ── Bottom HUD panel ──────────────────────────────────────────────────
        panel_x = (WIDTH - HUD_PANEL_W) // 2
        panel_y = HEIGHT - HUD_PANEL_H - 4

        # Panel background + border
        pygame.draw.rect(
            screen,
            (20, 18, 16),
            pygame.Rect(panel_x, panel_y, HUD_PANEL_W, HUD_PANEL_H),
        )
        pygame.draw.rect(
            screen,
            (65, 60, 52),
            pygame.Rect(panel_x, panel_y, HUD_PANEL_W, HUD_PANEL_H),
            2,
        )

        # Icon area width: 3 slots × (52+6) - 6 gap after last = 168px
        icon_area_w = len(_WEAPON_ORDER) * (HUD_ICON_W + 6) - 6

        # Weapon icons (left side)
        icons_x = panel_x + 10
        icons_y = panel_y + (HUD_PANEL_H - HUD_ICON_H) // 2
        _draw_weapon_icons(
            screen,
            icons_x,
            icons_y,
            self._weapon_icons,
            self.player.weapons_inventory,
            self.player.current_weapon,
        )

        # Face portrait (center of remaining space)
        remaining_left = panel_x + 10 + icon_area_w + 8
        remaining_w = HUD_PANEL_W - 10 - icon_area_w - 8 - 80
        face_cx = remaining_left + remaining_w // 2
        face_cy = panel_y + HUD_PANEL_H // 2
        face_r = HUD_FACE_SIZE // 2
        face_state = _get_face_state(self.player.hp, self.player.pain_timer)
        _draw_hud_face(screen, face_cx, face_cy, face_r, face_state)

        # HP display (right side), color shifts green → red as HP drops
        hp_val = max(0, int(self.player.hp))
        hp_r = min(255, max(60, 255 - (100 - hp_val) * 2))
        hp_g = min(255, max(20, int(hp_val * 1.8)))
        hp_color = (hp_r, hp_g, 30)
        hp_text = self.font.render(f"HP {hp_val}", True, hp_color)
        hp_rect = hp_text.get_rect(
            midright=(panel_x + HUD_PANEL_W - 10, panel_y + HUD_PANEL_H // 2)
        )
        screen.blit(hp_text, hp_rect)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw play scene.

        Args:
            screen: Pygame surface to draw on.
        """
        # Ground terrain (pre-baked surface — O(1) blit)
        screen.blit(self._ground, (0, 0))

        # Draw obstacles (above ground, below all entities)
        for obstacle in self._obstacles:
            obstacle.draw(screen, self.timer)

        # Draw blood decals (lowest entity layer - under corpses)
        for decal in self.blood_decals:
            decal.draw(screen)

        # Draw dead zombies (corpses) (above decals, below living entities)
        for corpse in self.dead_zombies:
            corpse.draw(screen)

        # Draw player
        self.player.draw(screen)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

        # Draw zombies
        for zombie in self.zombies:
            zombie.draw(screen)

        # Draw pickups
        for pickup in self.pickups:
            pickup.draw(screen)

        # Draw acid projectiles
        for projectile in self.acid_projectiles:
            projectile.draw(screen)

        # Draw blood particles (on top of everything except HUD)
        for particle in self.blood_particles:
            particle.draw(screen)

        self._draw_hud(screen)
