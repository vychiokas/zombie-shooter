"""Play scene for zombie shooter."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame

from game.core.constants import (
    BLOOD_PARTICLE_COUNT,
    BLOOD_PARTICLE_SPEED,
    CONTACT_DPS,
    HEIGHT,
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
from game.entities.pickup import Pickup
from game.entities.player import Player
from game.entities.zombie import Zombie
from game.systems.collisions import (
    check_acid_projectile_player_collisions,
    check_bullet_zombie_collisions,
    check_player_pickup_collisions,
    check_player_zombie_collisions,
)
from game.systems.spawner import ZombieSpawner

if TYPE_CHECKING:
    from game.core.game import Game


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
        import math

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
        import math

        from game.core.constants import (
            EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER,
            EXPLODER_EXPLOSION_DAMAGE_TO_ZOMBIES,
            EXPLODER_EXPLOSION_RADIUS,
            EXPLODER_PARTICLE_COUNT,
            EXPLODER_PARTICLE_SPEED,
        )
        from game.systems.collisions import check_collision_circle

        # Damage player if within radius
        if check_collision_circle(
            explosion_pos,
            EXPLODER_EXPLOSION_RADIUS,
            self.player.pos,
            self.player.radius,
        ):
            self.player.hp -= EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER

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

    def update(self, dt: float) -> None:
        """Update gameplay.

        Args:
            dt: Delta time in seconds.
        """
        self.timer += dt

        # Survival mode - no win condition, just track time alive
        # Spawn rate increases indefinitely based on self.timer

        self.player.update(dt)

        # Continuous shooting when mouse button held
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left mouse button held
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            bullets = self.player.shoot(mouse_pos)
            self.bullets.extend(bullets)

        # Update bullets and remove dead ones
        self.bullets = [b for b in self.bullets if b.update(dt)]

        # Update blood particles
        self.blood_particles = [p for p in self.blood_particles if p.update(dt)]

        # Update dead zombies (corpses)
        self.dead_zombies = [z for z in self.dead_zombies if z.update(dt)]

        # Update blood decals (pools)
        self.blood_decals = [d for d in self.blood_decals if d.update(dt)]

        # Spawn zombies
        if self.spawner.update(dt, self.timer) and len(self.zombies) < MAX_ZOMBIES:
            spawn_pos = self.spawner.get_spawn_position()
            variant = self.spawner.get_spawn_variant()
            self.zombies.append(Zombie(spawn_pos, variant))

        # Update zombies
        for zombie in self.zombies:
            zombie.update(dt, self.player.pos)

        # Collect acid projectiles from spitter zombies
        for zombie in self.zombies:
            if zombie.variant == "spitter" and zombie.pending_projectiles:
                for pos, direction in zombie.pending_projectiles:
                    self.acid_projectiles.append(AcidProjectile(pos, direction))
                zombie.pending_projectiles.clear()

        # Update acid projectiles and remove dead ones
        self.acid_projectiles = [p for p in self.acid_projectiles if p.update(dt)]

        # Spawn pickups on timer
        self.pickup_spawn_timer += dt
        if self.pickup_spawn_timer >= PICKUP_SPAWN_RATE:
            self.pickup_spawn_timer = 0.0
            # Random interior position with margin
            x = random.uniform(PICKUP_SPAWN_MARGIN, WIDTH - PICKUP_SPAWN_MARGIN)
            y = random.uniform(PICKUP_SPAWN_MARGIN, HEIGHT - PICKUP_SPAWN_MARGIN)
            spawn_pos = pygame.Vector2(x, y)
            # Random weapon type
            weapon_type = random.choice(list(WEAPON_STATS.keys()))
            self.pickups.append(Pickup(spawn_pos, weapon_type))

        # Update pickups and remove dead ones
        self.pickups = [p for p in self.pickups if p.update(dt)]

        # Player-pickup collisions
        colliding_pickups = check_player_pickup_collisions(
            self.player.pos, self.player.radius, self.pickups
        )
        if colliding_pickups:
            # Collect first colliding pickup
            pickup_idx = colliding_pickups[0]
            pickup = self.pickups[pickup_idx]
            self.player.add_weapon(pickup.weapon_type)  # Add to inventory
            self.player.current_weapon = pickup.weapon_type  # Switch to it
            # Remove collected pickup
            self.pickups = [p for i, p in enumerate(self.pickups) if i != pickup_idx]

        # Bullet-zombie collisions
        bullet_zombie_hits = check_bullet_zombie_collisions(self.bullets, self.zombies)

        # Remove hit bullets and zombies (reverse order to avoid index issues)
        bullets_to_remove = set()
        zombies_to_remove = set()
        for b_idx, z_idx in bullet_zombie_hits:
            zombie = self.zombies[z_idx]
            zombie.hp -= 1  # Reduce HP instead of instant kill
            bullets_to_remove.add(b_idx)

            # Only spawn gore and remove zombie if HP depleted
            if zombie.hp <= 0:
                # Check if exploder variant - trigger explosion BEFORE removal
                if zombie.variant == "exploder":
                    self.apply_explosion(zombie.pos)

                # Standard death handling (all variants)
                self.spawn_blood_splash(zombie.pos)  # Spawn blood particles
                self.blood_decals.append(BloodDecal(zombie.pos))  # Spawn blood pool
                self.dead_zombies.append(DeadZombie(zombie.pos))  # Spawn corpse
                zombies_to_remove.add(z_idx)
                self.kills += 1

        self.bullets = [
            b for i, b in enumerate(self.bullets) if i not in bullets_to_remove
        ]
        self.zombies = [
            z for i, z in enumerate(self.zombies) if i not in zombies_to_remove
        ]

        # Player-zombie collisions (damage over time)
        colliding_zombies = check_player_zombie_collisions(
            self.player.pos, self.player.radius, self.zombies
        )
        if colliding_zombies:
            damage = CONTACT_DPS * dt * len(colliding_zombies)
            self.player.hp -= damage

        # Acid projectile-player collisions
        acid_hits = check_acid_projectile_player_collisions(
            self.player.pos, self.player.radius, self.acid_projectiles
        )
        projectiles_to_remove = set()
        for p_idx in acid_hits:
            projectile = self.acid_projectiles[p_idx]
            self.player.hp -= projectile.damage
            projectiles_to_remove.add(p_idx)

        self.acid_projectiles = [
            p
            for i, p in enumerate(self.acid_projectiles)
            if i not in projectiles_to_remove
        ]

        # Check game over
        if self.player.hp <= 0:
            from game.scenes.game_over import GameOverScene

            self.game.change_scene(GameOverScene(self.game, self.kills, won=False))

    def draw(self, screen: pygame.Surface) -> None:
        """Draw play scene.

        Args:
            screen: Pygame surface to draw on.
        """
        # Dark gray background
        screen.fill((40, 40, 40))

        # Draw blood decals (lowest layer - under corpses)
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

        # HUD - HP (top-left)
        hp_text = self.font.render(f"HP: {int(self.player.hp)}", True, (255, 255, 255))
        screen.blit(hp_text, (10, 10))

        # HUD - Survival timer (top-center)
        timer_text = self.font.render(
            f"Survived: {self.timer:.1f}s", True, (255, 255, 255)
        )
        timer_rect = timer_text.get_rect(center=(WIDTH // 2, 25))
        screen.blit(timer_text, timer_rect)

        # HUD - Kills (top-right)
        kills_text = self.font.render(f"Kills: {self.kills}", True, (255, 255, 255))
        kills_rect = kills_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(kills_text, kills_rect)

        # HUD - Weapon (bottom-left)
        weapon_text = self.font.render(
            f"Weapon: {self.player.current_weapon.capitalize()}", True, (255, 255, 255)
        )
        screen.blit(weapon_text, (10, HEIGHT - 50))
