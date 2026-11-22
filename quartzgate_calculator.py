#!/usr/bin/env python3
"""
QuartzGate Parametric BOM & Cost Calculator
Calculates structural quantities (2m & 4m staggered modules), mass, brush-applied
bentonite slurry volume, and CAPEX for factory-produced opaque white fused silica firebreaks.
"""

import argparse
import math


def calculate_quartzgate(length_km: float, canopy_height_m: float, thickness_mm: float):
    if length_km <= 0 or canopy_height_m <= 0 or thickness_mm <= 0:
        raise ValueError("All dimensions (length_km, canopy_height_m, thickness_mm) must be positive.")

    # 1. Geometry & 50% Staggered 2m / 4m Module Layout
    total_length_m = length_km * 1000.0
    wall_height_m = canopy_height_m * 1.25  # 1.25x canopy clearance rule
    tilt_angle_deg = 60.0
    tilt_rad = math.radians(tilt_angle_deg)

    # Sloped incline length along the 60-degree A-frame face
    sloped_length_m = wall_height_m / math.sin(tilt_rad)
    lamella_width_m = 1.0  # Standard 1.0 m interlocking column width
    thickness_m = thickness_mm / 1000.0

    # Two opposing 60-degree faces form the A-frame
    sides = 2
    columns_per_side = math.ceil(total_length_m / lamella_width_m)
    total_columns = columns_per_side * sides

    # Alternating columns use 2m starter/cap pieces + 4m standard modules for 50% running bond
    half_columns = total_columns / 2.0
    # Unstaggered columns: ceil(sloped_length / 4.0) 4m modules
    mods_4m_col_a = math.ceil(sloped_length_m / 4.0)
    # Staggered columns: 2m starter + remaining 4m modules + optional 2m cap
    remaining_after_2m = max(0.0, sloped_length_m - 2.0)
    mods_4m_col_b = math.floor(remaining_after_2m / 4.0)
    has_top_2m_cap = (remaining_after_2m % 4.0) > 0.1
    mods_2m_col_b = 1 + (1 if has_top_2m_cap else 0)

    total_4m_modules = int(round(half_columns * (mods_4m_col_a + mods_4m_col_b)))
    total_2m_modules = int(round(half_columns * mods_2m_col_b))
    total_modules = total_4m_modules + total_2m_modules

    # 2. Material Densities & Masses
    # Opaque micro-bubbled white fused silica density (~2050 kg/m3)
    silica_density_kg_m3 = 2050.0
    mass_4m_module_kg = 4.0 * lamella_width_m * thickness_m * silica_density_kg_m3
    mass_2m_module_kg = 2.0 * lamella_width_m * thickness_m * silica_density_kg_m3
    total_silica_tonnes = (
        (total_4m_modules * mass_4m_module_kg) + (total_2m_modules * mass_2m_module_kg)
    ) / 1000.0

    # Internal Basalt Fiber Reinforced Polymer (BFRP) post-and-beam skeleton
    # Vertical center posts every 4.0 m + lower (1.0x base) & upper (0.35x base) horizontal cross-beams
    bays = math.ceil(total_length_m / 4.0)
    post_length_m = wall_height_m * 0.95
    base_span_m = (wall_height_m / math.tan(tilt_rad)) * 2.0
    upper_beam_span_m = base_span_m * 0.35
    total_bfrp_meters = bays * (post_length_m + base_span_m + upper_beam_span_m)
    bfrp_linear_mass_kg_m = 8.5  # Heavy-duty structural pultruded BFRP profile
    total_bfrp_tonnes = (total_bfrp_meters * bfrp_linear_mass_kg_m) / 1000.0

    # Hardware: Hourglass X-Keys & 15 cm Expanding Ground Shoes
    total_x_keys = total_modules * 2  # Two X-keys per stacked module
    total_ground_shoes = total_columns  # One 15 cm shoe per 1.0 m column base
    shoe_mass_kg = 2.4  # Galvanized/weathering steel 15 cm wedge anchor
    total_steel_tonnes = (total_ground_shoes * shoe_mass_kg) / 1000.0

    # Brush-Applied Bentonite & Basalt Slurry (vertical U-grooves + horizontal V-ridge joints)
    vertical_joint_meters = total_columns * sloped_length_m
    horizontal_joint_meters = total_modules * lamella_width_m
    slurry_liters = (vertical_joint_meters + horizontal_joint_meters) * 0.15  # ~0.15 L/m brushed coat

    # 3. Industrial CAPEX Estimate (Factory-Produced Prefab Model)
    cost_silica_eur = total_silica_tonnes * 1000.0 * 1.65
    cost_bfrp_eur = total_bfrp_meters * 18.00
    cost_hardware_eur = (total_ground_shoes * 14.0) + (total_x_keys * 4.5)
    cost_slurry_eur = slurry_liters * 1.20
    cost_logistics_install_eur = total_length_m * 180.0  # Rapid pilot-tool ground crew
    total_capex_eur = (
        cost_silica_eur
        + cost_bfrp_eur
        + cost_hardware_eur
        + cost_slurry_eur
        + cost_logistics_install_eur
    )

    # Benchmark: Conventional Wildfire Crisis Intervention + Restoration Cost
    wildfire_loss_low_eur = length_km * 10_000_000.0
    wildfire_loss_high_eur = length_km * 30_000_000.0

    # 4. Formatted Output Report
    print("=" * 68)
    print(f" QUARTZGATE BOM & CAPEX REPORT ({length_km:.1f} km Perimeter)")
    print("=" * 68)
    print(f"Target Canopy Height        : {canopy_height_m:.1f} m")
    print(f"Calibrated Wall Height      : {wall_height_m:.2f} m (1.25x rule)")
    print(f"60° Sloped Incline Length   : {sloped_length_m:.2f} m (50% Staggered 2m/4m Bond)")
    print(f"Effective Panel Thickness   : {thickness_mm:.0f} mm (Opaque White Fused Silica)")
    print("-" * 68)
    print("STRUCTURAL QUANTITIES:")
    print(f"  • 4.0m Standard Modules   : {total_4m_modules:,} pcs ({mass_4m_module_kg:,.1f} kg each)")
    print(f"  • 2.0m Starter/Cap Pieces : {total_2m_modules:,} pcs ({mass_2m_module_kg:,.1f} kg each)")
    print(f"  • Total Fused Silica Mass : {total_silica_tonnes:,.1f} tonnes")
    print(f"  • BFRP Internal Frame     : {total_bfrp_meters:,.0f} m ({total_bfrp_tonnes:,.1f} tonnes)")
    print(f"  • Hourglass X-Keys        : {total_x_keys:,} pcs")
    print(f"  • 15cm Ground Shoes       : {total_ground_shoes:,} pcs ({total_steel_tonnes:,.1f} tonnes)")
    print(f"  • Bentonite Slurry Seal   : {slurry_liters:,.0f} liters (Brush-applied)")
    print("-" * 68)
    print("ESTIMATED CAPEX (PREFAB FACTORY SUPPLY + RAPID INSTALL):")
    print(f"  • Fused Silica Modules    : €{cost_silica_eur:,.0f}")
    print(f"  • Basalt Fiber Frame      : €{cost_bfrp_eur:,.0f}")
    print(f"  • X-Keys & Ground Shoes   : €{cost_hardware_eur:,.0f}")
    print(f"  • Bentonite Slurry        : €{cost_slurry_eur:,.0f}")
    print(f"  • Transport & Install     : €{cost_logistics_install_eur:,.0f}")
    print(f"  ► TOTAL ESTIMATED CAPEX   : €{total_capex_eur:,.0f} (€{total_capex_eur/length_km:,.0f} / km)")
    print("-" * 68)
    print(f"Avoided Wildfire Damage     : €{wildfire_loss_low_eur:,.0f} – €{wildfire_loss_high_eur:,.0f}")
    print("=" * 68)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QuartzGate Parametric BOM Calculator")
    parser.add_argument("--km", type=float, default=10.0, help="Firewall perimeter length in km")
    parser.add_argument("--canopy", type=float, default=20.0, help="Average forest canopy height in meters")
    parser.add_argument("--thickness", type=float, default=12.0, help="Effective silica thickness in mm")
    args = parser.parse_args()

    calculate_quartzgate(args.km, args.canopy, args.thickness)
