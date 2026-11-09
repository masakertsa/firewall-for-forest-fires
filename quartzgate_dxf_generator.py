#!/usr/bin/env python3
"""
QuartzGate Parametric DXF CAD Generator
Generates a 1:1 millimeter DXF cross-section of a fused silica lamella
with male/female tongue-and-groove joints, internal dovetail groove,
symmetrical hourglass (X-key) lock, and steel horizontal beam.
"""

import argparse


def generate_lamella_dxf(
    filename: str = "quartzgate-parametric-lamella.dxf",
    width_mm: float = 1000.0,
    thickness_mm: float = 50.0,
    groove_depth_mm: float = 8.0,
    groove_mouth_mm: float = 20.0,
    groove_base_mm: float = 30.0,
) -> None:
    half_w = width_mm / 2.0
    m_half = groove_mouth_mm / 2.0
    b_half = groove_base_mm / 2.0

    # Male tongue (left side) & Female U-groove (right side)
    tongue_len = 15.0
    tongue_h = thickness_mm * 0.31
    y_bot = (thickness_mm - tongue_h) / 2.0
    y_top = y_bot + tongue_h

    ugroove_depth = 20.0
    ugroove_h = thickness_mm * 0.35
    ug_bot = (thickness_mm - ugroove_h) / 2.0
    ug_top = ug_bot + ugroove_h

    lines = []

    def add_line(layer: str, x1: float, y1: float, x2: float, y2: float) -> None:
        lines.append(
            f"0\nLINE\n8\n{layer}\n"
            f"10\n{x1:.3f}\n20\n{y1:.3f}\n30\n0.0\n"
            f"11\n{x2:.3f}\n21\n{y2:.3f}\n31\n0.0"
        )

    # 1. Quartz Lamella Profile
    # Fire-facing exterior (top edge, y = thickness_mm)
    add_line("QUARTZ_LAMELLA", -half_w, thickness_mm, half_w, thickness_mm)
    # Left side with male tongue
    add_line("QUARTZ_LAMELLA", -half_w, thickness_mm, -half_w, y_top)
    add_line("QUARTZ_LAMELLA", -half_w, y_top, -half_w - tongue_len, y_top)
    add_line("QUARTZ_LAMELLA", -half_w - tongue_len, y_top, -half_w - tongue_len, y_bot)
    add_line("QUARTZ_LAMELLA", -half_w - tongue_len, y_bot, -half_w, y_bot)
    add_line("QUARTZ_LAMELLA", -half_w, y_bot, -half_w, 0.0)
    # Right side with female U-groove
    add_line("QUARTZ_LAMELLA", half_w, thickness_mm, half_w, ug_top)
    add_line("QUARTZ_LAMELLA", half_w, ug_top, half_w - ugroove_depth, ug_top)
    add_line("QUARTZ_LAMELLA", half_w - ugroove_depth, ug_top, half_w - ugroove_depth, ug_bot)
    add_line("QUARTZ_LAMELLA", half_w - ugroove_depth, ug_bot, half_w, ug_bot)
    add_line("QUARTZ_LAMELLA", half_w, ug_bot, half_w, 0.0)
    # Sheltered interior bottom edge with central dovetail groove
    add_line("QUARTZ_LAMELLA", -half_w, 0.0, -m_half, 0.0)
    add_line("QUARTZ_LAMELLA", -m_half, 0.0, -b_half, groove_depth_mm)
    add_line("QUARTZ_LAMELLA", -b_half, groove_depth_mm, b_half, groove_depth_mm)
    add_line("QUARTZ_LAMELLA", b_half, groove_depth_mm, m_half, 0.0)
    add_line("QUARTZ_LAMELLA", m_half, 0.0, half_w, 0.0)

    # 2. Symmetrical Hourglass (X-Key) Lock (flush waist at y = 0.0)
    add_line("HOURGLASS_X_KEY", -b_half, groove_depth_mm, b_half, groove_depth_mm)
    add_line("HOURGLASS_X_KEY", b_half, groove_depth_mm, m_half, 0.0)
    add_line("HOURGLASS_X_KEY", m_half, 0.0, b_half, -groove_depth_mm)
    add_line("HOURGLASS_X_KEY", b_half, -groove_depth_mm, -b_half, -groove_depth_mm)
    add_line("HOURGLASS_X_KEY", -b_half, -groove_depth_mm, -m_half, 0.0)
    add_line("HOURGLASS_X_KEY", -m_half, 0.0, -b_half, groove_depth_mm)

    # 3. Structural Steel Horizontal Beam (200 x 60 mm)
    beam_half = 100.0
    beam_h = 60.0
    add_line("STEEL_BEAM", -beam_half, 0.0, -m_half, 0.0)
    add_line("STEEL_BEAM", -m_half, 0.0, -b_half, -groove_depth_mm)
    add_line("STEEL_BEAM", -b_half, -groove_depth_mm, b_half, -groove_depth_mm)
    add_line("STEEL_BEAM", b_half, -groove_depth_mm, m_half, 0.0)
    add_line("STEEL_BEAM", m_half, 0.0, beam_half, 0.0)
    add_line("STEEL_BEAM", beam_half, 0.0, beam_half, -beam_h)
    add_line("STEEL_BEAM", beam_half, -beam_h, -beam_half, -beam_h)
    add_line("STEEL_BEAM", -beam_half, -beam_h, -beam_half, 0.0)

    dxf_content = (
        "0\nSECTION\n2\nHEADER\n0\nENDSEC\n"
        "0\nSECTION\n2\nENTITIES\n"
        + "\n".join(lines)
        + "\n0\nENDSEC\n0\nEOF\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(dxf_content)
    print(f"Generated DXF file: {filename} ({width_mm}x{thickness_mm} mm)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QuartzGate Parametric DXF Generator")
    parser.add_argument("--out", type=str, default="quartzgate-parametric-lamella.dxf", help="Output DXF filename")
    parser.add_argument("--width", type=float, default=1000.0, help="Lamella width in mm (default: 1000)")
    parser.add_argument("--thickness", type=float, default=50.0, help="Lamella thickness in mm (default: 50)")
    args = parser.parse_args()

    generate_lamella_dxf(
        filename=args.out,
        width_mm=args.width,
        thickness_mm=args.thickness,
    )
