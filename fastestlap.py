import fastf1
import pandas as pd


session = fastf1.get_session(2025, "China", 'R') 
session.load(telemetry=False, weather=False)


fastest_laps = []
for driver in session.drivers:
    drv_lap = session.laps.pick_drivers(driver).pick_fastest()
    if not drv_lap.empty:
        fastest_laps.append(drv_lap)


fastest_laps_df = pd.DataFrame(fastest_laps)


fastest_laps_df = fastest_laps_df.sort_values(by="LapTime")


leader_time = fastest_laps_df.iloc[0]["LapTime"]


lap_times = []
for _, row in fastest_laps_df.iterrows():
    driver = row["Driver"]
    lap_time = row["LapTime"]

    gap = (lap_time - leader_time).total_seconds()
    
    lap_times.append([driver, str(lap_time)[10:], f"{gap:.2f}s"]) 


lap_times_df = pd.DataFrame(lap_times, columns=['Sigla', 'Tempo', 'Gap'])
lap_times_df.iloc[0, 2] = "0.00s" 

print("Tabela de Voltas Mais Rápidas:")
print(lap_times_df)
