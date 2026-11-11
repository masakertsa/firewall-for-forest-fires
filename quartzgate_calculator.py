#!/usr/bin/env python3
"""
QuartzGate Bill of Materials (BOM) & ROI Calculator
Calculates opaque white fused silica lamellae, internal basalt fiber composite
post-and-beam frame, one-way ridge pressure flaps, hourglass X-keys,
self-locking uplift wedge ground shoes, and lifecycle cost comparison.
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
    white_silica_price_per_m2_eur: float = 45.0,  # Reduced via In-Situ Solar Foundry
    basalt_price_per_ton_eur: float = 2800.0,
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

    # Opaque micro-bubbled white fused silica mass (density ~ 2050 kg/m3)
    thickness_m = glass_thickness_mm / 1000.0
    total_glass_volume_m3 = total_glass_area_m2 * thickness_m
    total_glass_mass_tons = (total_glass_volume_m3 * 2050.0) / 1000.0

    # 2. Internal basalt fiber composite post-and-beam skeleton & hardware
    num_posts = math.ceil(total_line_m / post_spacing_m) + 1
    post_height_m = wall_height_m * 0.85
    cross_beam_length_m = (wall_height_m / math.tan(tilt_rad)) * 1.1
    upper_ridge_beam_m = total_line_m
    total_basalt_length_m = (num_posts * (post_height_m + cross_beam_length_m)) + upper_ridge_beam_m
    # Approx 14 kg/m for structural hollow basalt fiber composite profile (vs 45 kg/m steel)
    total_basalt_mass_tons = (total_basalt_length_m * 14.0) / 1000.0

    # Hourglass X-keys (2 per lamella: upper & lower beam interface)
    total_x_keys = total_lamellae * 2
    # Self-locking uplift wedge ground shoes (1 per lamella)
    total_ground_shoes = total_lamellae
    # One-way upward-opening ridge pressure/ember flaps (1 per 1.0m apex section)
    total_ridge_flaps = lamellae_per_side

    # 3. Cost Estimation (CAPEX)
    glass_cost_eur = total_glass_area_m2 * white_silica_price_per_m2_eur
    basalt_cost_eur = total_basalt_mass_tons * basalt_price_per_ton_eur
    hardware_cost_eur = (
        (total_x_keys * 10.0)
        + (total_ground_shoes * 22.0)  # Expanding wedge anchor shoe
        + (total_ridge_flaps * 15.0)   # Basalt-hinged ridge flapper plate
    )
    solar_foundry_and_hydro_eur = 2_200_000.0 * (wall_length_km / 10.0)
    total_capex_eur = (
        glass_cost_eur
        + basalt_cost_eur
        + hardware_cost_eur
        + solar_foundry_and_hydro_eur
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
        "total_basalt_mass_tons": round(total_basalt_mass_tons, 1),
        "total_x_keys": total_x_keys,
        "total_ground_shoes": total_ground_shoes,
        "total_ridge_flaps": total_ridge_flaps,
        "glass_cost_eur": round(glass_cost_eur),
        "basalt_cost_eur": round(basalt_cost_eur),
        "hardware_cost_eur": round(hardware_cost_eur),
        "foundry_hydro_eur": round(solar_foundry_and_hydro_eur),
        "total_capex_eur": round(total_capex_eur),
        "crisis_min_eur": round(crisis_min_eur),
        "crisis_max_eur": round(crisis_max_eur),
    }


def print_report(data: dict) -> None:
    print("=" * 68)
    print("🔥 QUARTZGATE STRUCTURAL & ECONOMIC REPORT (OPAQUE WHITE SILICA)")
    print("=" * 68)
    print(f"Protected Perimeter Length : {data['wall_length_km']} km (Total line: {data['total_line_m']} m)")
    print(f"Local Canopy Height        : {data['canopy_height_m']} m -> Wall Height (Hw): {data['wall_height_m']} m")
    print(f"60° Lamella Slant Length   : {data['slant_length_m']} m")
    print("-" * 68)
    print("📦 BILL OF MATERIALS (BOM)")
    print(f"White Silica Lamellae      : {data['total_lamellae']:,} pcs ({data['total_glass_area_m2']:,} m²)")
    print(f"Opaque White Silica Mass   : {data['total_glass_mass_tons']:,} metric tons (2,050 kg/m³)")
    print(f"Basalt Composite Skeleton  : {data['num_posts']:,} frames ({data['total_basalt_mass_tons']:,} tons)")
    print(f"Hourglass (X-Key) Locks    : {data['total_x_keys']:,} pcs")
    print(f"Uplift Wedge Ground Shoes  : {data['total_ground_shoes']:,} pcs")
    print(f"One-Way Ridge Ember Flaps  : {data['total_ridge_flaps']:,} pcs")
    print("-" * 68)
    print("💶 ESTIMATED CAPEX vs. WILDFIRE CRISIS COST")
    print(f"In-Situ White Silica Cost  : €{data['glass_cost_eur']:,}")
    print(f"Basalt Fiber Skeleton      : €{data['basalt_cost_eur']:,}")
    print(f"X-Keys, Wedges & Flaps     : €{data['hardware_cost_eur']:,}")
    print(f"Solar Foundry & Hydro Grid : €{data['foundry_hydro_eur']:,}")
    print(f"TOTAL QUARTZGATE CAPEX     : €{data['total_capex_eur']:,} (Low-maintenance OPEX)")
    print(f"Unprotected Crisis Loss    : €{data['crisis_min_eur']:,} – €{data['crisis_max_eur']:,} per event")
    print("=" * 68)


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
