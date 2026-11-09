#!/usr/bin/env python3
"""
QuartzGate Bill of Materials (BOM) & ROI Calculator
Calculates fused silica lamellae, internal steel post-and-beam frame,
hourglass X-keys, ground shoes, and lifecycle cost comparison.
"""

import math
import argparse


def calculate_quartzgate(
    wall_length_km: float = 10.0,
    canopy_height_m: float = 20.0,
    glass_thickness_mm: float = 50.0,
    lamella_width_m: float = 1.0,
    overlap_count: int = 8,
    overlap_length_m: float = 8.0,
    post_spacing_m: float = 4.0,
    silica_price_per_m2_eur: float = 65.0,
    steel_price_per_ton_eur: float = 1800.0,
) -> dict:
    # 1. Wall geometry (60-degree A-frame)
    wall_height_m = canopy_height_m * 1.25
    tilt_rad = math.radians(60.0)
    slant_length_m = wall_height_m / math.sin(tilt_rad)

    # Effective linear wall length including 8m parallel overlaps
    base_length_m = wall_length_km * 1000.0
    extra_overlap_m = overlap_count * overlap_length_m
    total_line_m = base_length_m + extra_overlap_m

    # Two opposing 60-degree sides per A-frame line
    lamellae_per_side = math.ceil(total_line_m / lamella_width_m)
    total_lamellae = lamellae_per_side * 2
    area_per_lamella_m2 = lamella_width_m * slant_length_m
    total_glass_area_m2 = total_lamellae * area_per_lamella_m2

    # Fused silica mass (density ~ 2200 kg/m3)
    thickness_m = glass_thickness_mm / 1000.0
    total_glass_volume_m3 = total_glass_area_m2 * thickness_m
    total_glass_mass_tons = (total_glass_volume_m3 * 2200.0) / 1000.0

    # 2. Internal steel post-and-beam skeleton & X-keys
    num_posts = math.ceil(total_line_m / post_spacing_m) + 1
    post_height_m = wall_height_m * 0.85
    cross_beam_length_m = (wall_height_m / math.tan(tilt_rad)) * 1.1
    total_steel_length_m = num_posts * (post_height_m + cross_beam_length_m)
    # Approx 45 kg/m for structural S355 H-beam
    total_steel_mass_tons = (total_steel_length_m * 45.0) / 1000.0

    # Hourglass X-keys (2 per lamella: upper & lower beam interface)
    total_x_keys = total_lamellae * 2
    # Ground shoes (1 per lamella)
    total_ground_shoes = total_lamellae

    # 3. Cost Estimation (CAPEX)
    glass_cost_eur = total_glass_area_m2 * silica_price_per_m2_eur
    steel_cost_eur = total_steel_mass_tons * steel_price_per_ton_eur
    x_key_and_shoe_cost_eur = (total_x_keys * 12.0) + (total_ground_shoes * 18.0)
    gravity_hydro_and_hub_eur = 1_500_000.0 * (wall_length_km / 10.0)
    total_capex_eur = (
        glass_cost_eur
        + steel_cost_eur
        + x_key_and_shoe_cost_eur
        + gravity_hydro_and_hub_eur
    )

    # Traditional wildfire crisis cost benchmark (scaled by length)
    scale = wall_length_km / 10.0
    crisis_min_eur = 100_000_000.0 * scale
    crisis_max_eur = 300_000_000.0 * scale

    return {
        "wall_length_km": wall_length_km,
        "canopy_height_m": canopy_height_m,
        "wall_height_m": round(wall_height_m, 2),
        "slant_length_m": round(slant_length_m, 2),
        "total_line_m": round(total_line_m, 1),
        "total_lamellae": total_lamellae,
        "total_glass_area_m2": round(total_glass_area_m2, 1),
        "total_glass_mass_tons": round(total_glass_mass_tons, 1),
        "num_posts": num_posts,
        "total_steel_mass_tons": round(total_steel_mass_tons, 1),
        "total_x_keys": total_x_keys,
        "total_ground_shoes": total_ground_shoes,
        "glass_cost_eur": round(glass_cost_eur),
        "steel_cost_eur": round(steel_cost_eur),
        "hardware_cost_eur": round(x_key_and_shoe_cost_eur),
        "total_capex_eur": round(total_capex_eur),
        "crisis_min_eur": round(crisis_min_eur),
        "crisis_max_eur": round(crisis_max_eur),
    }


def print_report(data: dict) -> None:
    print("=" * 64)
    print("🔥 QUARTZGATE STRUCTURAL & ECONOMIC REPORT")
    print("=" * 64)
    print(f"Protected Perimeter Length : {data['wall_length_km']} km (Total line: {data['total_line_m']} m)")
    print(f"Local Canopy Height        : {data['canopy_height_m']} m -> Wall Height (Hw): {data['wall_height_m']} m")
    print(f"60° Lamella Slant Length   : {data['slant_length_m']} m")
    print("-" * 64)
    print("📦 BILL OF MATERIALS (BOM)")
    print(f"Fused Silica Lamellae      : {data['total_lamellae']:,} pcs ({data['total_glass_area_m2']:,} m²)")
    print(f"Total Fused Silica Mass    : {data['total_glass_mass_tons']:,} metric tons")
    print(f"Internal Steel Frames      : {data['num_posts']:,} post-and-beam sets ({data['total_steel_mass_tons']:,} tons)")
    print(f"Hourglass (X-Key) Locks    : {data['total_x_keys']:,} pcs")
    print(f"60° Metallic Ground Shoes  : {data['total_ground_shoes']:,} pcs")
    print("-" * 64)
    print("💶 ESTIMATED CAPEX vs. WILDFIRE CRISIS COST")
    print(f"Fused Silica Glass Cost    : €{data['glass_cost_eur']:,}")
    print(f"Internal Steel Skeleton    : €{data['steel_cost_eur']:,}")
    print(f"X-Keys & Ground Shoes      : €{data['hardware_cost_eur']:,}")
    print(f"TOTAL QUARTZGATE CAPEX     : €{data['total_capex_eur']:,} (50-yr OPEX: €0)")
    print(f"Unprotected Crisis Loss    : €{data['crisis_min_eur']:,} – €{data['crisis_max_eur']:,} per event")
    print("=" * 64)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QuartzGate BOM & Cost Calculator")
    parser.add_argument("--km", type=float, default=10.0, help="Perimeter length in km (default: 10.0)")
    parser.add_argument("--canopy", type=float, default=20.0, help="Local canopy height in meters (default: 20.0)")
    parser.add_argument("--thickness", type=float, default=50.0, help="Glass thickness in mm (default: 50.0)")
    args = parser.parse_args()

    result = calculate_quartzgate(
        wall_length_km=args.km,
        canopy_height_m=args.canopy,
        glass_thickness_mm=args.thickness,
    )
    print_report(result)
