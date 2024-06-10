import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axisartist.parasite_axes import HostAxes
import time as timeLib
import requests
from datetime import datetime
import math
import os

# Configurazione
URL = "https://api.wheretheiss.at/v1/satellites/25544"
MAX_DATA_STORE_LEN = 5 # Numero massimo di dati da memorizzare 
POLLING_DELAY = 10 # In secondi
REQ_TIMEOUT = 7 # Secondi massimi prima che la richiesta venga interrotta
OUTPUT_DPI = 300 # Dpi dell'output (grandezza dell'immagine). Abbassare se diventa troppo lento a renderizzare

# Store di dati.
time = [] # Tempo (in unix), asse x
latitude = [] # Latitudine
longitude = [] # Longitudine
altitude= [] # Altitudine

os.unsetenv("SESSION_MANAGER") # Disattiva l'avviso "Qt: Session management error: None of the authentication protocols specified are supported"

def toDate(unix, pos):
  return datetime.fromtimestamp(unix).strftime("%H:%M:%S")

FORMATTER = FuncFormatter(toDate)


def updateLocation():
  try:
    res = requests.get(URL, timeout=REQ_TIMEOUT).json()
    pos = {}
    if (len(time) > MAX_DATA_STORE_LEN): time.pop(0)
    if (len(latitude) > MAX_DATA_STORE_LEN): latitude.pop(0)
    if (len(longitude) > MAX_DATA_STORE_LEN): longitude.pop(0)
    if (len(altitude) > MAX_DATA_STORE_LEN): altitude.pop(0)
    time.append(math.floor(datetime.timestamp(datetime.now())))
    latitude.append(float(res['latitude']))
    longitude.append(float(res['longitude']))
    altitude.append(round(float(res['altitude']), 1))
    print("> ✅ Posizione ottenuta con successo")
    return True # Successo
  except ValueError as e:
    print(e)
    print("> ⚠️ Errore nell'ottenimento della posizione")
    timeLib.sleep(1)
    return False # Errore


while True:
  print("> Ottenendo la positizone")
  if not updateLocation(): continue
  print("> Generando il grafico")

  try:
    # Ottieni figura
    fig = plt.figure(figsize=(10, 6))

    # Creazione del grafico
    host = fig.add_axes([0.15, 0.1, 0.65, 0.8], axes_class=HostAxes)
    par1 = host.get_aux_axes(viewlim_mode=None, sharex=host)
    par2 = host.get_aux_axes(viewlim_mode=None, sharex=host)

    # Imposta la posizione dei margini e etichette per host e parassiti
    host.axis["right"].set_visible(False)
    par1.axis["right"].set_visible(True)
    par1.axis["right"].major_ticklabels.set_visible(True)
    par1.axis["right"].label.set_visible(True)
    par2.axis["right2"] = par2.new_fixed_axis(loc="right", offset=(78, 0))

    # Imposta le etichette
    host.set_xlabel("Tempo")
    host.set_ylabel("Latitudine")
    par1.set_ylabel("Longitudine")
    par2.set_ylabel("Altitudine (Km)")

    host.xaxis.set_major_formatter(FORMATTER)

    host.set_title("Posizione dell'ISS")

    latp, = host.plot(time, latitude, label="Latitudine", marker='o')
    lonp, = par1.plot(time, longitude, label="Longitudine", marker='o')
    altp, = par2.plot(time, altitude, label="Altitudine", marker='o', color="green")

    host.set_xticks(time)
    host.set_yticks(latitude)
    par1.set_yticks(longitude)
    par2.set_yticks(altitude)

    host.yaxis.get_label().set_color(latp.get_color())
    par1.yaxis.get_label().set_color(lonp.get_color())
    par2.yaxis.get_label().set_color(altp.get_color())
    host.tick_params(axis='y')
    par1.tick_params(axis='y')
    par2.tick_params(axis='y')

    host.legend(labelcolor="linecolor")
    host.grid(True, alpha=0.5)
    plt.xticks(rotation=20)

    plt.savefig('output.png', dpi=OUTPUT_DPI)
    plt.clf()

    print("> ✅ Grafico generato con successo")
    print(f"> Prossimo aggiornamento in {POLLING_DELAY} secondi...")
    timeLib.sleep(POLLING_DELAY)
  except ValueError as e:
    print(e)
    print(f"> ❌ Errore durante la generazione del grafico. Ritentando in 2 secondi...")
    timeLib.sleep(2)
