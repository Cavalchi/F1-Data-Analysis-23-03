import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import fastf1
from fastf1 import plotting


def configurar_fastf1():
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.figsize'] = (15, 6)
    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)
    return fastf1.get_session(2025, 'China', 'R')


def criar_grafico_estategia_pneus(session):
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


def analise_corrida():
    print("Inicializando análise...")
    session = configurar_fastf1()
    data = carregar_dados(session)
    print("\n Gerando gráficos...")
   
    criar_grafico_estategia_pneus(session)
    print("\n Análise concluída!")

if __name__ == "__main__":
    analise_corrida()
