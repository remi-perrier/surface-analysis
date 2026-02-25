"""Analysis of Yann's tube surface measurement (1ER_x10_xt1x5_avg3.datx).

Produces height maps at each decomposition stage and saves them as PNG files
in an output/ directory next to this script.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from surface_analysis import Surface, Transforms

DATX_PATH = (
    "/Users/rperrier/Documents/temp/SurfaceObservation/examples/1ER_x10_xt1x5_avg3.datx"
)
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def save_plot(surface: Surface, filename: str, title: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    surface.plot(ax=ax)
    ax.set_title(title)
    fig.savefig(OUTPUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {filename}")


def main() -> None:
    # Load raw measurement
    raw = Surface.from_datx(DATX_PATH)
    print(f"Raw surface: {raw}")
    print(f"  NaN ratio: {raw.nan_ratio:.1%}")
    save_plot(raw, "01_raw.png", "Raw measurement")

    # Interpolate missing data
    interpolated = raw.apply(Transforms.Interpolation.Linear())
    print(f"\nAfter interpolation: {interpolated}")
    save_plot(interpolated, "02_interpolated.png", "After linear interpolation")

    # Remove form (polynomial degree 2)
    form_removed = interpolated.apply(Transforms.Projection.Polynomial(degree=2))
    print(f"\nAfter form removal: {form_removed}")
    save_plot(form_removed, "03_form_removed.png", "Form removed (polynomial degree 2)")

    # Extract waviness (lowpass at 0.8 mm cutoff)
    waviness = form_removed.apply(
        Transforms.Filtering.Gaussian(cutoff=0.8, mode="lowpass")
    )
    print(f"\nWaviness: {waviness}")
    save_plot(waviness, "04_waviness.png", "Waviness (lowpass, cutoff=0.8 mm)")

    # Extract roughness (highpass at 0.8 mm cutoff)
    roughness = form_removed.apply(Transforms.Filtering.Gaussian(cutoff=0.8))
    print(f"\nRoughness: {roughness}")
    save_plot(roughness, "05_roughness.png", "Roughness (highpass, cutoff=0.8 mm)")

    # Extract micro-roughness (highpass at 0.025 mm cutoff)
    micro_roughness = roughness.apply(Transforms.Filtering.Gaussian(cutoff=0.025))
    print(f"\nMicro-roughness: {micro_roughness}")
    save_plot(
        micro_roughness,
        "06_micro_roughness.png",
        "Micro-roughness (highpass, cutoff=0.025 mm)",
    )

    # Summary of ISO 25178 parameters at each stage
    print("\n--- ISO 25178 parameters ---")
    stages = {
        "Form removed": form_removed,
        "Waviness": waviness,
        "Roughness": roughness,
        "Micro-roughness": micro_roughness,
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
