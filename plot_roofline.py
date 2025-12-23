# plot_roofline.py - Generate publication-quality roofline chart
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load your data
df = pd.read_csv('roofline_data.csv')

# Chart parameters (realistic GPU: A100-like)
PEAK_FLOPS = 2e12  # 2 TFLOP/s
peak_tflops = PEAK_FLOPS / 1e12

# Compute roofline bounds
def compute_roofline(bw_gbps):
    """Arithmetic intensity where compute = memory bound"""
    return (bw_gbps * 1e9 / 8) / PEAK_FLOPS  # bytes/s / flops/s = ops/byte

roof_points = []
for bw in df['bandwidth_gbps'].unique():
    ai_knee = compute_roofline(bw)
    peak_perf = PEAK_FLOPS / 1e12  # TFLOP/s
    roof_points.append({'bw_gbps': bw, 'ai_knee': ai_knee, 'peak_perf': peak_perf})

roof_df = pd.DataFrame(roof_points)

# Create the chart
fig, ax = plt.subplots(figsize=(10, 7))

# Plot data points - sequential (blue)
seq_df = df[df['access_pattern'] == 'sequential']
ax.scatter(seq_df['arithmetic_intensity'], seq_df['achieved_flops']/1e12, 
           c='blue', s=60, alpha=0.7, label='Sequential', zorder=3)

# Plot data points - random (red)
rand_df = df[df['access_pattern'] == 'random']
ax.scatter(rand_df['arithmetic_intensity'], rand_df['achieved_flops']/1e12, 
           c='red', s=60, alpha=0.7, label='Random', zorder=3)

# Plot roofline bounds
for _, roof in roof_df.iterrows():
    bw_gbs = roof['bw_gbps'] / 8  # Convert to GB/s for label
    # Horizontal compute roof
    ax.hlines(roof['peak_perf'], 0, 10, colors='black', linestyles='-', linewidth=2)
    # Vertical memory wall
    ax.vlines(roof['ai_knee'], 0, roof['peak_perf'], colors='black', linestyles='-', linewidth=2)
    # Diagonal roofline
    ax.plot([roof['ai_knee'], 10], [roof['peak_perf'], roof['peak_perf']], 
            'k--', alpha=0.5, linewidth=1)
    
    # Label roofs
    ax.text(roof['ai_knee']*1.2, roof['peak_perf']*0.9, 
            f'{bw_gbs:.0f}GB/s', fontsize=9, ha='left')

# Styling
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Arithmetic Intensity (FLOP/Byte)', fontsize=12)
ax.set_ylabel('Performance (TFLOP/s)', fontsize=12)
ax.set_title('Roofline Model: Sequential vs Random Access Patterns', fontsize=14, pad=20)
ax.grid(True, alpha=0.3)
ax.legend(loc='lower right')

# Annotations
ax.text(0.1, peak_tflops*0.8, 'Compute-bound', rotation=0, fontsize=11, 
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
ax.text(2, peak_tflops*0.3, 'Memory-bound', rotation=90, fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))

plt.tight_layout()
plt.savefig('roofline_chart.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ roofline_chart.png saved! Perfect for your blog.")
print(f"Sequential points: {len(seq_df)} compute-bound, {len(seq_df)-len(seq_df[seq_df['regime']=='compute-bound'])} memory-bound")
print(f"Random points: {len(rand_df)} compute-bound, {len(rand_df)-len(rand_df[rand_df['regime']=='compute-bound'])} memory-bound")
