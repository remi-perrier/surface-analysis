"""Compare surface_analysis results with MountainsMap reference values.

Reference: .reference/mountainsmap_reference.md
Sample: .reference/11PM_x10_xt1x5_avg3.datx (Raw evaporator n°11)
"""

from __future__ import annotations

from surface_analysis import Surface, Transforms


def pct_err(ours: float, ref: float) -> str:
    if ref == 0:
        return "N/A"
    err = (ours - ref) / abs(ref) * 100
    return f"{err:+.2f}%"


def main() -> None:
    surf = Surface.from_datx(".reference/11PM_x10_xt1x5_avg3.datx")
    print(f"Surface: {surf}")
    print()

    # -------------------------------------------------------------------------
    # BOX 1 — Primary surface (plane leveling only)
    # MountainsMap: Opération F = Redressé (TLS), Filtre S = Gaussien 2.5 µm
    # -------------------------------------------------------------------------
    primary_plane = surf.apply(
        Transforms.Projection.Polynomial(degree=1, mode="residual"),
    )

    ref_box1 = {"Sa": 24.42, "Sq": 29.06, "Ssk": 0.6532, "Sk": 56.28}

    print("=" * 72)
    print("BOX 1 — Primary surface (plane leveling)")
    print("MountainsMap: F=TLS plane, S-filter=Gaussian 2.5 µm")
    print("=" * 72)
    print(f"  {'Param':<8} {'MountainsMap':>14} {'Ours':>14} {'Error':>10}")
    print(f"  {'-' * 8} {'-' * 14} {'-' * 14} {'-' * 10}")
    for param, ref_val in ref_box1.items():
        if param == "Sk":
            ours_val = primary_plane.Sk * 1000  # mm → µm
        else:
            ours_val = getattr(primary_plane, param) * (
                1000 if param in ("Sa", "Sq") else 1
            )
        print(
            f"  {param:<8} {ref_val:>14.4f} {ours_val:>14.4f} {pct_err(ours_val, ref_val):>10}"
        )

    # Box 1 volume parameters — MountainsMap Vv = Vv(p=10%) = Vvc + Vvv
    ref_box1_vol = {"Vv(10%)": 0.04506, "Vvv": 0.001271}
    print()
    print("  Volume parameters (mm³/mm²):")
    af_box1 = primary_plane.abbott_firestone
    vv10_box1 = af_box1.Vvc + af_box1.Vvv
    print(
        f"  {'Vv(10%)':<8} {ref_box1_vol['Vv(10%)']:>14.6f} {vv10_box1:>14.6f} {pct_err(vv10_box1, ref_box1_vol['Vv(10%)']):>10}"
    )
    print(
        f"  {'Vvv':<8} {ref_box1_vol['Vvv']:>14.6f} {af_box1.Vvv:>14.6f} {pct_err(af_box1.Vvv, ref_box1_vol['Vvv']):>10}"
    )
    print()

    # -------------------------------------------------------------------------
    # BOX 2 — Roughness surface (Poly 2 + HP λc=0.8 mm)
    # MountainsMap: after full pipeline LSP2 + FS + FL
    # -------------------------------------------------------------------------
    dec = surf.decompose(
        form="polynomial",
        lambda_c=0.8,
        lambda_s=0.0025,
        interpolation="nearest",
    )

    ref_box2 = {"Sa": 5.327, "Sq": 6.687, "Ssk": 0.1306, "Sk": 17.08}

    print("=" * 72)
    print("BOX 2 — Roughness surface (Poly 2 + Gaussian HP λc=0.8 mm)")
    print("MountainsMap: LSP2 + FS (λs=2.5µm) + FL (λc=0.8mm)")
    print("=" * 72)
    print(f"  {'Param':<8} {'MountainsMap':>14} {'Ours':>14} {'Error':>10}")
    print(f"  {'-' * 8} {'-' * 14} {'-' * 14} {'-' * 10}")
    for param, ref_val in ref_box2.items():
        if param == "Sk":
            ours_val = dec.roughness.Sk * 1000  # mm → µm
        else:
            ours_val = getattr(dec.roughness, param) * (
                1000 if param in ("Sa", "Sq") else 1
            )
        print(
            f"  {param:<8} {ref_val:>14.4f} {ours_val:>14.4f} {pct_err(ours_val, ref_val):>10}"
        )

    # Box 2 volume parameters — MountainsMap Vv = Vv(p=10%) = Vvc + Vvv
    ref_box2_vol = {"Vv(10%)": 0.008933, "Vvv": 0.0007142}
    print()
    print("  Volume parameters (mm³/mm²):")
    af_box2 = dec.roughness.abbott_firestone
    vv10_box2 = af_box2.Vvc + af_box2.Vvv
    print(
        f"  {'Vv(10%)':<8} {ref_box2_vol['Vv(10%)']:>14.7f} {vv10_box2:>14.7f} {pct_err(vv10_box2, ref_box2_vol['Vv(10%)']):>10}"
    )
    print(
        f"  {'Vvv':<8} {ref_box2_vol['Vvv']:>14.7f} {af_box2.Vvv:>14.7f} {pct_err(af_box2.Vvv, ref_box2_vol['Vvv']):>10}"
    )
    print()

    # -------------------------------------------------------------------------
    # Abbott-Firestone — Volume parameters (from PDF page 4, left side)
    # "Réglage du filtre: Sans filtrage" — computed on roughness surface
    # -------------------------------------------------------------------------
    ref_af = {
        "Vmp": 0.0003423,
        "Vmc": 0.006007,
        "Vvc": 0.008219,
        "Vvv": 0.0007142,
    }

    print("=" * 72)
    print("ABBOTT-FIRESTONE — Volume parameters (on roughness surface)")
    print("=" * 72)
    print(f"  {'Param':<8} {'MountainsMap':>14} {'Ours':>14} {'Error':>10}  Unit")
    print(f"  {'-' * 8} {'-' * 14} {'-' * 14} {'-' * 10}  ----")
    for param, ref_val in ref_af.items():
        ours_val = getattr(af_box2, param)
        print(
            f"  {param:<8} {ref_val:>14.7f} {ours_val:>14.7f} {pct_err(ours_val, ref_val):>10}  mm³/mm²"
        )

    # Sk parameters
    print()
    print("  Sk parameters:")
    print(
        f"  {'Sk':<8} {ref_box2['Sk']:>14.2f} {af_box2.Sk * 1000:>14.2f} {pct_err(af_box2.Sk * 1000, ref_box2['Sk']):>10}  µm"
    )
    print(f"  {'Smr1':<8} {'':>14} {af_box2.Smr1:>14.2f}  %")
    print(f"  {'Smr2':<8} {'':>14} {af_box2.Smr2:>14.2f}  %")
    print(f"  {'Spk':<8} {'':>14} {af_box2.Spk * 1000:>14.2f}  µm")
    print(f"  {'Svk':<8} {'':>14} {af_box2.Svk * 1000:>14.2f}  µm")


if __name__ == "__main__":
    main()
