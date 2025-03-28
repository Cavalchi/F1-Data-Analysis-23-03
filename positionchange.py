import matplotlib.pyplot as plt
import fastf1.plotting
import fastf1


session = fastf1.get_session(2025, "China", 'R') 
session.load(telemetry=False, weather=False)


fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')


fig, ax = plt.subplots(figsize=(10.0, 6.0))
for drv in session.drivers:
    drv_laps = session.laps.pick_drivers(drv) 
    
 
    abb = drv_laps['Driver'].iloc[0]
    

    style = fastf1.plotting.get_driver_style(identifier=abb, style=['color', 'linestyle'], session=session)
    

    ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)

ax.set_ylim([20.5, 0.5])
ax.set_yticks([1, 5, 10, 15, 20]) 
ax.set_xlabel('Volta') 
ax.set_ylabel('Posição')  
ax.legend(bbox_to_anchor=(1.0, 1.02))  
plt.tight_layout()

plt.show()
