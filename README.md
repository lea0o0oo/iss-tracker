# Tracker ISS

Indice

- [Introduzione](#introduzione)
- [Configurazione degli script](#configurazione-degli-script) (⚠️ Consiglio di leggerlo)
- Scripts
  - [Script base](#script-base)
  - [Script con GUI](#script-con-gui) (⚠️ Consiglio di leggerlo prima di usarlo)

## Introduzione

Questo progetto scolastico fatto in python serve a tracciare latitudine, longitudine e altitudine della ISS. <br />
È stato pensato per essere eseguito su un Rasberry Pi per essere collegato ad uno schermo informativo, ma può essere eseguito su qualsiasi computer. <br />
Per questo motivo ho fatto 2 versioni dello script: <br /><br />

1. La prima versione `mainBase.py` è quella più semplice, e genera un grafico `output.png` con latitudine, logitudine e altitudine in funzione del tempo.
2. La seconda versione `gtk.py`, costruita su `mainBase.py` genera una interfaccia grafica fatta con il toolkit [GTK](https://www.gtk.org)

## Configurazione degli script

Ogni versione dello script, dopo gli import, ha delle "costanti" che possono essere utilizzate per impostare alcuni parametri

`URL` - Non è da cambiare - Url da dove vengono presi i dati della iss <br />
`MAX_DATA_STORE_LEN` - Numero massimo di valori che vengono salvati. Più questo numero è grande e più informazioni verranno tenute nel grafico. <br />
`POLLING_DELAY` - Delay in secondi tra gli aggiornamenti. Il rate limit della API è di circa 1 richiesta al secondo. <br />
`REQ_TIMEOUT` - Timeout in secondi prima che la richiesta viene interrotta. Se la richiesta viene interrotta, lo script ne effettuerà un'altra dopo 2 secondi. <br />
`OUTPUT_DPI` - I DPI del grafico. All'aumentare di questo numero aumenta la dimensione dell'immagine. Consiglio di non andare sotto i _300_ altrimenti l'immagine verrà tagliata

#### SOLO PER GUI

##### Alcuni parametri validi solo per la versione con GUI <br />

`LIVE_URL_ID` - Id della diretta YouTube <br />
`LAYOUT` - Tipo di layout. Può avere 2 valori: "horizontal" o "vertical". <br />
`FULLSCREEN` - Scegli se mostrare la finestra in fullscreen o meno. Si può uscire dal fullscreen con la combinazione `Alt` + `F4`

# Script base

Questo script è la versione "base": genera un grafico con Latitudine, Longitudine e Altitudine in funzione del tempo trascorso.

Librerie **esterne** usate:

- `matplotlib`
- `requests`

Installazione<br />
`pip install requests matplotlib` <br />

ℹ️ **Assicurarsi che siano alla versione più recente!**

### Esecuzione

Per eseguire lo script basta fare <br />
`python mainBase.py`

# Script con GUI

Questa versione dello script genera una interfaccia grafica con a sinistra / sopra (varia dal layout specificato nella configurazione) il grafico della latitudine, longitudine e altitudine in funzione del tempo e a destra / sotto la live stream della ISS

![Demo GUI](https://i.imgur.com/FchIelE.png)

```
⚠️ NOTA 1: Al primo avvio darà errore perché non trova il file output.png.
Bisogna aspettare un pochino fino a quando non genera questo file.
Una volta generato, basterà chiudere e riaprire lo script e tutto dovrebbe andare correttamente.
```

```
⚠️ NOTA 2: Nella seconda e terza linea ho messo come versioni di gtk e webkit2 rispettivamente 3.0 e 4.1
Questi valori possono cambiare da dispositivo a dispositivo, quindi se esce un errore del tipo
"ValueError: Namespace WebKit2/Gtk not available for version x" significa
che Gtk/Webkit2 è installato ma non è stata selezionata la versione corretta.
L'importante è che sia Gtk che Webkit2 stiano nelle loro major release (gtk 3.x webkit 4.x)
```

Per la GUI ho usato come toolkit GTK in modo da tenere tutto in un singolo file e avere migliori prestazioni sulla memoria rispetto ad un browser.

**Librerie esterne**

- `matplotlib`
- `requests`
- `gtk`

Installazione<br />
`pip install requests matplotlib` <br />
ℹ️ **Assicurarsi che siano alla versione più recente!**

`sudo apt install libwebkit2gtk-4.0-dev` - Webkit2 4.0 (Debian e derivate) <br />
`sudo pacman -S webkit2gtk-4.1` - Webkit2 4.0 (con pacman, generalmente disponibile su Arch) <br />
Gtk dovrebbe essere già installato su linux (come la maggior parte delle librerie)

### Esecuzione

Per eseguire lo script basta fare <br />
`python gtk.py`
