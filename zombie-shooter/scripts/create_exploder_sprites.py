"""Generate orange/yellow-tinted exploder zombie sprites."""

from __future__ import annotations

from pathlib import Path

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

script_dir = Path(__file__).resolve().parent
assets_dir = script_dir / "src/assets/zombies"
exploder_dir = script_dir / "src/assets/zombies/exploder"
exploder_dir.mkdir(parents=True, exist_ok=True)

directions = ["walk_down", "walk_up", "walk_left", "walk_right"]

for direction in directions:
    original_path = assets_dir / f"{direction}.png"
    original = pygame.image.load(str(original_path))

    # Create orange-tinted version
    tinted = original.copy()
    orange_overlay = pygame.Surface(original.get_size()).convert_alpha()
    orange_overlay.fill((255, 140, 0, 0))  # Orange tint (explosive color)
    tinted.blit(orange_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    # Add yellow highlight for extra visibility
    yellow_overlay = pygame.Surface(original.get_size()).convert_alpha()
    yellow_overlay.fill((200, 180, 0, 0))  # Yellow highlight
    tinted.blit(yellow_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    # Save
    output_path = exploder_dir / f"{direction}.png"
    pygame.image.save(tinted, str(output_path))
    print(f"Created {output_path}")

print("Exploder sprites created successfully!")
