"""Generate blue-tinted tank zombie sprites."""

from __future__ import annotations

from pathlib import Path

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

script_dir = Path(__file__).resolve().parent
assets_dir = script_dir / "src/assets/zombies"
tank_dir = script_dir / "src/assets/zombies/tank"
tank_dir.mkdir(parents=True, exist_ok=True)

directions = ["walk_down", "walk_up", "walk_left", "walk_right"]

for direction in directions:
    original_path = assets_dir / f"{direction}.png"
    original = pygame.image.load(str(original_path))

    # Create blue-tinted version
    tinted = original.copy()
    blue_overlay = pygame.Surface(original.get_size()).convert_alpha()
    blue_overlay.fill((80, 120, 255, 0))  # Blue tint (tank armor color)
    tinted.blit(blue_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    # Add gray tint for "armored" metallic look
    gray_overlay = pygame.Surface(original.get_size()).convert_alpha()
    gray_overlay.fill((60, 60, 60, 0))  # Slight gray for metallic look
    tinted.blit(gray_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    # Save
    output_path = tank_dir / f"{direction}.png"
    pygame.image.save(tinted, str(output_path))
    print(f"Created {output_path}")

print("Tank sprites created successfully!")
