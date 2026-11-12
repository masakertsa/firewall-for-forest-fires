#!/usr/bin/env python3
"""
QuartzGate Parametric BOM & Cost Calculator
Calculates structural quantities, mass, and realistic CAPEX for factory-produced
opaque white fused silica firebreak walls (without on-site foundry overhead).
"""

import argparse
import math


def calculate_quartzgate(length_km: float, canopy_height_m: float, thickness_mm: float):
    # 1. Geometry & Dimensions
    total_length_m = length_km * 1000.0
    wall_height_m = canopy_height_m * 1.25  # 1.25x canopy clearance rule
    tilt_angle_deg = 60.0
    tilt_rad = math.radians(tilt_angle_deg)

    # Sloped panel length along the 60-degree A-frame incline
    sloped_length_m = wall_height_m / math.sin(tilt_rad)
    lamella_width_m = 1.0  # Standard 1.0 m interlocking slice width
    thickness_m = thickness_mm / 1000.0

    # Two opposing 60-degree faces form the A-frame
    sides = 2
    lamellae_per_side = math.ceil(total_length_m / lamella_width_m)
    total_lamellae = lamellae_per_side * sides

    # 2. Material Densities & Masses
    # Opaque micro-bubbled white fused silica density (~2050 kg/m3 vs 2200 for clear)
    silica_density_kg_m3 = 2050.0
    single_lamella_vol_m3 = sloped_length_m * lamella_width_m * thickness_m
    single_lamella_mass_kg = single_lamella_vol_m3 * silica_density_kg_m3
    total_silica_tonnes = (total_lamellae * single_lamella_mass_kg) / 1000.0

    # Internal Basalt Fiber Reinforced Polymer (BFRP) post-and-beam skeleton
    # Vertical center posts every 4.0 m + 2 horizontal cross-beams per bay
    bays = math.ceil(total_length_m / 4.0)
    post_length_m = wall_height_m * 0.95
    beam_length_m = (wall_height_m / math.tan(tilt_rad)) * 2.0
    total_bfrp_meters = bays * (post_length_m + 2.0 * beam_length_m)
    bfrp_linear_mass_kg_m = 6.5  # Heavy-duty structural pultruded profile
    total_bfrp_tonnes = (total_bfrp_meters * bfrp_linear_mass_kg_m) / 1000.0

    # Hardware: Hourglass X-Keys & 15 cm Expanding Ground Shoes
    total_x_keys = total_lamellae * 2  # Upper & lower beam locks per lamella
    total_ground_shoes = total_lamellae  # One 15 cm shoe per lamella base
    shoe_mass_kg = 2.4  # Galvanized/weathering steel 15 cm wedge anchor
    total_steel_tonnes = (total_ground_shoes * shoe_mass_kg) / 1000.0

    # Bentonite labyrinth seal & basalt wool base blanket
    bentonite_kg = total_lamellae * sloped_length_m * 1.2

    # 3. Realistic Industrial CAPEX Estimate (Factory-Produced Prefab Model)
    # Estimates based on bulk industrial fused silica (~€3.5/kg) & BFRP (~€18/m)
    cost_silica_eur = total_silica_tonnes * 1000.0 * 3.50
    cost_bfrp_eur = total_bfrp_meters * 18.00
    cost_hardware_eur = (total_ground_shoes * 14.0) + (total_x_keys * 6.5)
    cost_logistics_install_eur = total_length_m * 220.0  # Rapid pilot-tool ground crew
    total_capex_eur = (
        cost_silica_eur + cost_bfrp_eur + cost_hardware_eur + cost_logistics_install_eur
    )

    # Benchmark: Conventional Wildfire Crisis Intervention + Restoration Cost
    wildfire_loss_low_eur = length_km * 10_000_000.0
    wildfire_loss_high_eur = length_km * 30_000_000.0

    # 4. Formatted Output Report
    print("=" * 65)
    print(f" QUARTZGATE BOM & CAPEX REPORT ({length_km:.1f} km Perimeter)")
    print("=" * 65)
    print(f"Target Canopy Height      : {canopy_height_m:.1f} m")
    print(f"Calibrated Wall Height    : {wall_height_m:.2f} m (1.25x rule)")
    print(f"60° Sloped Panel Length   : {sloped_length_m:.2f} m")
    print(f"Lamella Thickness         : {thickness_mm:.0f} mm (Opaque White Fused Silica)")
    print("-" * 65)
    print("STRUCTURAL QUANTITIES:")
    print(f"  • Quartz Lamellae (1m)  : {total_lamellae:,} pcs ({total_silica_tonnes:,.1f} tonnes)")
    print(f"  • Single Panel Mass     : {single_lamella_mass_kg:,.1f} kg")
    print(f"  • BFRP Internal Frame   : {total_bfrp_meters:,.0f} m ({total_bfrp_tonnes:,.1f} tonnes)")
    print(f"  • Hourglass X-Keys      : {total_x_keys:,} pcs")
    print(f"  • 15cm Ground Shoes     : {total_ground_shoes:,} pcs ({total_steel_tonnes:,.1f} tonnes)")
    print(f"  • Bentonite Sealant     : {bentonite_kg:,.0f} kg")
    print("-" * 65)
    print("ESTIMATED CAPEX (PREFAB FACTORY SUPPLY + RAPID INSTALL):")
    print(f"  • Fused Silica Panels   : €{cost_silica_eur:,.0f}")
    print(f"  • Basalt Fiber Frame    : €{cost_bfrp_eur:,.0f}")
    print(f"  • X-Keys & Ground Shoes : €{cost_hardware_eur:,.0f}")
    print(f"  • Transport & Install   : €{cost_logistics_install_eur:,.0f}")
    print(f"  ► TOTAL ESTIMATED CAPEX : €{total_capex_eur:,.0f} (€{total_capex_eur/length_km:,.0f} / km)")
    print("-" * 65)
    print(f"Avoided Wildfire Damage   : €{wildfire_loss_low_eur:,.0f} – €{wildfire_loss_high_eur:,.0f}")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QuartzGate Parametric BOM Calculator")
    parser.add_argument("--km", type=float, default=10.0, help="Firewall perimeter length in km")
    parser.add_argument("--canopy", type=float, default=20.0, help="Average forest canopy height in meters")
    parser.add_argument("--thickness", type=float, default=50.0, help="Quartz lamella thickness in mm")
    args = parser.parse_args()

    calculate_quartzgate(args.km, args.canopy, args.thickness)
