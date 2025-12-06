import fastf1
import pandas as pd
import numpy as np

# Enable cache (and handle if already enabled)
try:
    fastf1.Cache.enable_cache('f1_cache')
except:
    pass

# Analysis Parameters
SEASON = 2025
ROUNDS = range(1, 24) # Race 1 to Race 23
DRIVERS = ['VER', 'NOR', 'PIA'] # Championship Contenders (Verstappen, Norris, Piastri)

data_list = []

print(f"{SEASON} Season Data collection Started...")
print("-" * 60)

for r in ROUNDS:
    current_race_name = f"Round {r}"
    try:
        # --- QUALIFYING DATA ---
        session_q = fastf1.get_session(SEASON, r, 'Q')
        session_q.load(telemetry=False, weather=False, messages=False)
        current_race_name = session_q.event.EventName
        
        print(f"\n📍 [{r}/23] Processing: {current_race_name}")
        
        # Get Pole Position Lap Time
        pole_lap = session_q.laps.pick_fastest()
        if pole_lap is None or pd.isna(pole_lap['LapTime']):
            print("Pole lap not found, skipping this round.")
            continue
            
        pole_time = pole_lap['LapTime']
        
        # --- RACE DATA ---
        session_r = fastf1.get_session(SEASON, r, 'R')
        session_r.load(telemetry=False, weather=False, messages=False)
        
        # Determine the Race Winner to use as a baseline
        try:
            # Try to get the winner from official results
            winner_abbr = session_r.results.loc[session_r.results['Position']==1, 'Abbreviation'].iloc[0]
        except:
            # Fallback: Pick the driver with the fastest lap if results are missing
            winner_abbr = session_r.laps.pick_fastest()['Driver']
            
        # Calculate Winner's Average Race Pace (excluding slow laps)
        winner_laps = session_r.laps.pick_driver(winner_abbr).pick_quicklaps()
        winner_mean_pace = winner_laps['LapTime'].mean()

        # Extract data for specific drivers
        for driver in DRIVERS:
            row = {'Round': r, 'RaceName': current_race_name, 'Driver': driver}
            
            # Qualifying Gap Analysis
            d_laps_q = session_q.laps.pick_driver(driver).pick_quicklaps()
            if not d_laps_q.empty:
                d_best_q = d_laps_q['LapTime'].min()
                # Calculate gap to pole in seconds
                row['Quali_Gap'] = (d_best_q - pole_time).total_seconds()
            else:
                row['Quali_Gap'] = None

            # Race Pace Analysis
            d_laps_r = session_r.laps.pick_driver(driver).pick_quicklaps()
            if not d_laps_r.empty:
                d_mean_pace = d_laps_r['LapTime'].mean()
                # Calculate gap to winner's average pace
                row['Race_Pace_Diff'] = (d_mean_pace - winner_mean_pace).total_seconds()
            else:
                row['Race_Pace_Diff'] = None
            
            data_list.append(row)
            print(f"    Data Added: {driver}")

    except Exception as e:
        print(f"    Critical Error (Round {r}): {e}")
        continue

# --- SAVE DATA ---
if len(data_list) > 0:
    df = pd.DataFrame(data_list)
    df.to_csv('f1_2025_champ_data.csv', index=False)
    print("-" * 60)
    print(f"SUCCESS! Total {len(df)} rows saved to 'f1_2025_champ_data.csv'.")
    print("You can now run 'visualize.py'.")
else:
    print("-" * 60)
    print("ERROR: No data collected. Please check the logs above.")