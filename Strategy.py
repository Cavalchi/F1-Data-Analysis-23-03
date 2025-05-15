import os
import pandas as pd
import matplotlib.pyplot as plt
import fastf1
from fastf1 import plotting

# Configuração inicial do FastF1 e cache
def configurar_fastf1():
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.figsize'] = (15, 6)
    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)
    return fastf1.get_session(2025, 'China', 'R')

# Gera tabela com as voltas mais rápidas
def gerar_tabela_voltas_rapidas(session):
    fastest_laps = []
    for driver in session.drivers:
        drv_lap = session.laps.pick_drivers(driver).pick_fastest()
        if not drv_lap.empty:
            fastest_laps.append(drv_lap)

    fastest_laps_df = pd.DataFrame(fastest_laps).sort_values(by="LapTime")
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

# Gera gráfico e tabela com a estratégia de pneus (stints)
def criar_grafico_estrategia_pneus(session):
    laps = session.laps
    stints = laps[['Driver', 'Stint', 'Compound', 'LapNumber']]
    stints = stints.groupby(['Driver', 'Stint', 'Compound']).count().reset_index()
    stints = stints.rename(columns={'LapNumber': 'StintLength'})
    stints['MudancaComposto'] = stints['Compound'] != stints.groupby('Driver')['Compound'].shift(1)
    stints['StintGroup'] = stints.groupby('Driver')['MudancaComposto'].cumsum()
    stints_agrupados = stints.groupby(['Driver', 'StintGroup', 'Compound']).agg({'StintLength': 'sum'}).reset_index()
    stints_agrupados = stints_agrupados.drop(['StintGroup'], axis=1)

    print("\nDados dos Stints Agrupados:")
    print(stints_agrupados.to_string(index=False))



# Gera gráfico de posição por volta
def gerar_grafico_posicoes(session):
    plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')
    fig, ax = plt.subplots(figsize=(10.0, 6.0))

    for drv in session.drivers:
        drv_laps = session.laps.pick_drivers(drv)
        abb = drv_laps['Driver'].iloc[0]
        style = plotting.get_driver_style(identifier=abb, style=['color', 'linestyle'], session=session)
        ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)

    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Volta')
    ax.set_ylabel('Posição')
    ax.legend(bbox_to_anchor=(1.0, 1.02))
    plt.tight_layout()
    plt.show()

# Função principal
def analise_corrida():
    print("Inicializando análise...")
    session = configurar_fastf1()
    session.load(telemetry=False, weather=False)

    gerar_tabela_voltas_rapidas(session)
    criar_grafico_estrategia_pneus(session)
    
    gerar_grafico_posicoes(session)

    print("\nAnálise concluída!")

if __name__ == "__main__":
    analise_corrida()
