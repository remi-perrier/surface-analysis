"""Analysis of Yann's tube surface measurement (1ER_x10_xt1x5_avg3.datx).

Produces 2D height maps (PNG), 3D static views (PNG), and 3D interactive
plots (HTML) at each decomposition stage. Saved in an output/ directory.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from surface_analysis import Surface

DATX_PATH = (
    "/Users/rperrier/Documents/temp/SurfaceObservation/examples/1ER_x10_xt1x5_avg3.datx"
)
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def save_plot(surface: Surface, base_name: str, title: str) -> None:
    # 2D height map
    ax = surface.plot(title=title)
    ax.figure.savefig(OUTPUT_DIR / f"{base_name}.png", dpi=150, bbox_inches="tight")
    plt.close(ax.figure)
    print(f"  Saved {base_name}.png")

    # 3D static (matplotlib)
    ax3 = surface.plot_3d(title=title)
    ax3.figure.savefig(OUTPUT_DIR / f"{base_name}_3d.png", dpi=150, bbox_inches="tight")
    plt.close(ax3.figure)
    print(f"  Saved {base_name}_3d.png")

    # 3D interactive (plotly)
    fig_html = surface.plot_3d_interactive(title=title)
    fig_html.write_html(OUTPUT_DIR / f"{base_name}_3d.html")
    print(f"  Saved {base_name}_3d.html")


def main() -> None:
    # Load raw measurement
    raw = Surface.from_datx(DATX_PATH)
    print(f"Raw surface: {raw}")
    print(f"  NaN ratio: {raw.nan_ratio:.1%}")
    save_plot(raw, "01_raw", "Raw measurement")

    # Decompose using ISO 25178-3 F/S/L pipeline
    dec = raw.decompose(
        form="polynomial",
        lambda_c=0.8,
        lambda_s=0.025,
        interpolation="nearest",
    )

    save_plot(dec.form, "02_form", "Form (polynomial degree 2)")
    save_plot(dec.waviness, "03_waviness", "Waviness (λ > 0.8 mm)")
    save_plot(dec.roughness, "04_roughness", "Roughness (0.025 < λ < 0.8 mm)")
    save_plot(
        dec.micro_roughness,
        "05_micro_roughness",
        "Micro-roughness (λ < 0.025 mm)",
    )

    # Summary of ISO 25178 parameters at each stage
    print("\n--- ISO 25178 parameters ---")
    stages = {
        "Waviness": dec.waviness,
        "Roughness": dec.roughness,
        "Micro-roughness": dec.micro_roughness,
    }
    header = f"{'Stage':<20} {'Sa (µm)':>10} {'Sq (µm)':>10} {'Ssk':>10} {'Sku':>10} {'Sdq':>10}"
    print(header)
    print("-" * len(header))
    for name, s in stages.items():
        print(
            f"{name:<20} "
            f"{s.Sa * 1000:>10.4f} "
            f"{s.Sq * 1000:>10.4f} "
            f"{s.Ssk:>10.4f} "
            f"{s.Sku:>10.4f} "
            f"{s.Sdq:>10.4f}"
        )

    print(f"\nAll figures saved to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
