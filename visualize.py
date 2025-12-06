import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Visualization Settings
plt.style.use('dark_background')
sns.set_context("talk") # Increase font size for readability

# Driver Color Palette
driver_colors = {
    'VER': '#061D42',  # Red Bull Blue
    'NOR': '#FF8000',  # McLaren Orange
    'PIA': '#F4D73B'   # Distinctive Yellow 
}

try:
    # Read Data
    df = pd.read_csv('f1_2025_champ_data.csv')
    
    # Create Subplots (2 Rows, 1 Column)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), sharex=True)
    
    # --- PLOT 1: QUALIFYING PACE GAP ---
    sns.lineplot(
        data=df, x='Round', y='Quali_Gap', hue='Driver', 
        palette=driver_colors, marker='o', linewidth=3, ax=ax1
    )
    
    ax1.set_title('2025 Championship Battle: Gap to Pole Position (Qualifying)', fontsize=16, fontweight='bold', pad=20)
    ax1.set_ylabel('Gap (Seconds)\n(Lower is better)')
    ax1.axhline(0, color='white', linestyle='--', alpha=0.5, label='Pole Time')
    ax1.grid(True, alpha=0.2)
    ax1.legend(title='Driver', loc='upper right')
    
    # Limit Y-axis for better readability
    ax1.set_ylim(bottom=-0.1, top=1.5) 

    # --- PLOT 2: RACE PACE DIFF ---
    sns.lineplot(
        data=df, x='Round', y='Race_Pace_Diff', hue='Driver', 
        palette=driver_colors, marker='s', linewidth=3, ax=ax2
    )
    
    ax2.set_title('Race Pace Deficit (vs. Winner)', fontsize=16, fontweight='bold', pad=20)
    ax2.set_xlabel('Race Number (1-23)')
    ax2.set_ylabel('Avg Lap Delta (s)\n(0 = Winner\'s Pace)')
    ax2.axhline(0, color='white', linestyle='--', alpha=0.5, label='Winner Pace')
    ax2.grid(True, alpha=0.2)
    ax2.get_legend().remove() # Legend already exists in top plot

    # Race numbers on X-axis
    unique_races = df[['Round', 'RaceName']].drop_duplicates().sort_values('Round')
    ax2.set_xticks(unique_races['Round'])
    ax2.set_xticklabels(unique_races['Round'], rotation=0)

    plt.tight_layout()
    
    # Save Plot
    plt.savefig('2025_Championship_Analysis.png', dpi=300)
    print("Plot succesfully saved as: '2025_Championship_Analysis.png'")
    
    # Show Plot
    plt.show()

except FileNotFoundError:
    print("ERROR: 'f1_2025_champ_data.csv' not found.")
    print("Please run 'collect_data.py' first to download the data.")