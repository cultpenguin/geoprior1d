"""Quick test to verify geoprior1d functionality."""

from geoprior1d import generate_prior
import os

print("Testing geoprior1d module...")
print("-" * 50)

# Test with minimal parameters
input_file = "examples/data/daugaard_matlab.xlsx"
n_realizations = 10  # Small number for quick test
depth_max = 90
depth_step = 1

print(f"Input file: {input_file}")
print(f"Realizations: {n_realizations}")
print(f"Depth range: 0-{depth_max}m")
print("-" * 50)

try:
    # Run prior generator (no plotting for quick test)
    filename, flag_vector = generate_prior(
        input_data=input_file,
        Nreals=n_realizations,
        dmax=depth_max,
        dz=depth_step,
        doPlot=0
    )

    print("\n" + "=" * 50)
    print("✓ SUCCESS!")
    print("=" * 50)
    print(f"✓ Generated {n_realizations} realizations")
    print(f"✓ Output file: {filename}")
    print(f"✓ File size: {os.path.getsize(filename) / 1024:.2f} KB")

    if flag_vector[0] == 1:
        print("⚠️  Warning: Some constraints could not be satisfied")
    print(f"✓ Average constraint satisfaction attempts: {flag_vector[2]:.1f}")

except Exception as e:
    print(f"\n✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
