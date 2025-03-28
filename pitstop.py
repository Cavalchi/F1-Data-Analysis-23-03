import fastf1
import pandas as pd

session = fastf1.get_session(2025, "China", 'R') 
session.load()
laps = session.laps

stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
stints = stints.rename(columns={"LapNumber": "StintLength"})
pit_stop_info = []

for _, row in stints.iterrows():
    driver = row["Driver"]
    
    stint_length = row["StintLength"]
    
    stop_lap = row["Stint"] + stint_length - 1
    
    compound = row["Compound"]
    
    pit_stop_info.append([driver, stop_lap, compound])

pit_df = pd.DataFrame(pit_stop_info, columns=['Sigla', 'Volta de Parada', 'Composto'])


print("\nTabela de Pit Stops e Compostos de Pneus:")
print(pit_df)
