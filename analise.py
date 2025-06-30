# --- F1 Analysis Engine v3.0 (Com Análise Visual e Foco em Storytelling) ---
# Autor: João Pedro Cavalchi de Carvalho

import os
import pandas as pd
import matplotlib.pyplot as plt
import fastf1
from fastf1 import plotting


def carregar_sessao_corrida(ano, nome_gp, tipo_sessao='R'):
    print(f"Configurando ambiente para {ano} {nome_gp} ({tipo_sessao})...")
    plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False)
    plt.style.use('seaborn-v0_8-darkgrid')
    
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)
    
    print("Carregando dados da sessão... Isso pode levar alguns momentos.")
    try:
        session = fastf1.get_session(ano, nome_gp, tipo_sessao)
        session.load()
        print("Dados carregados com sucesso!")
        return session
    except Exception as e:
        print(f"!!! ERRO ao carregar dados: {e}")
        print("!!! Verifique se a corrida já aconteceu e se o nome do GP está correto.")
        return None


def plotar_comparativo_voltas_rapidas(session):
    """NOVA FUNÇÃO: Gera um gráfico de barras comparando as voltas mais rápidas."""
    print("\n--- Análise 1: Gráfico Comparativo de Voltas Mais Rápidas ---")
    
    laps = session.laps.pick_quicklaps().reset_index()
    fastest_laps = laps.loc[laps.groupby('Driver')['LapTime'].idxmin()]
    fastest_laps = fastest_laps[['Driver', 'LapTime', 'Team']].sort_values(by='LapTime')

    top_10_fastest = fastest_laps.head(10)

    fig, ax = plt.subplots(figsize=(12, 7))
    
    lap_times_seconds = top_10_fastest['LapTime'].dt.total_seconds()
    drivers = top_10_fastest['Driver']
    team_colors = [fastf1.plotting.get_team_color(team, session=session) for team in top_10_fastest['Team']]

    bars = ax.barh(drivers, lap_times_seconds, color=team_colors, edgecolor='black')
    ax.invert_yaxis() 
    ax.set_xlabel("Tempo da Volta (em segundos)")
    ax.set_ylabel("Piloto")
    ax.set_title(f"Comparativo de Voltas Mais Rápidas - {session.event.EventName} {session.event.year}")
    
    for i, bar in enumerate(bars):
        lap_time_str = f"{int(lap_times_seconds.iloc[i]//60)}:{lap_times_seconds.iloc[i]%60:06.3f}"
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2.0, lap_time_str, va='center')

    plt.tight_layout()
    plt.show()

def analisar_estrategia_pneus_plot(session):
    print("\n--- Análise 2: Gráfico de Estratégia de Pneus ---")
    drivers = [session.get_driver(driver)["Abbreviation"] for driver in session.drivers]
    stints = session.laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
    stints = stints.rename(columns={"LapNumber": "StintLength"})
    fig, ax = plt.subplots(figsize=(10, 6))
    for driver in drivers:
        driver_stints = stints[stints["Driver"] == driver]
        previous_stint_end = 0
        for _, stint in driver_stints.iterrows():
            plt.barh(y=driver, width=stint["StintLength"], left=previous_stint_end, color=fastf1.plotting.COMPOUND_COLORS[stint["Compound"]], edgecolor="black", fill=True)
            previous_stint_end += stint["StintLength"]
    ax.set_xlabel("Número da Volta")
    ax.set_ylabel("Piloto")
    ax.set_title(f"Estratégia de Pneus - {session.event['EventName']} {session.event.year}")
    plt.tight_layout()
    plt.show()

def analisar_posicao_por_volta(session):
    print("\n--- Análise 3: Gráfico de Posição por Volta ---")
    fig, ax = plt.subplots(figsize=(10.0, 6.0))
    for drv in session.drivers:
        try:
            drv_laps = session.laps.pick_drivers(drv)
            if drv_laps.empty: continue
            abb = drv_laps['Driver'].iloc[0]
            color = fastf1.plotting.get_team_color(drv_laps['Team'].iloc[0], session=session)
            if pd.isnull(color): color = 'gray'
            ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, color=color)
        except Exception as e:
            print(f"Não foi possível plotar o piloto {drv}: {e}")
    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Número da Volta')
    ax.set_ylabel('Posição')
    ax.set_title(f"Batalha por Posições - {session.event['EventName']} {session.event.year}")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def main():

    ANO_DA_CORRIDA = 2025
    NOME_DO_GP = "Chinese Grand Prix"
    TIPO_DE_SESSAO = 'R'
    
    sessao_de_corrida = carregar_sessao_corrida(ANO_DA_CORRIDA, NOME_DO_GP, TIPO_DE_SESSAO)

    if sessao_de_corrida:
        # 1. Nova análise visual de voltas rápidas
        plotar_comparativo_voltas_rapidas(sessao_de_corrida)
        
        # 2. Análise de estratégia de pneus
        analisar_estrategia_pneus_plot(sessao_de_corrida)
        
        # 3. Análise da batalha por posições
        analisar_posicao_por_volta(sessao_de_corrida)
        
        print("\nAnálise completa!")
    else:
        print("\nA análise não pôde ser concluída pois os dados da sessão não foram carregados.")

if __name__ == "__main__":
    main()
