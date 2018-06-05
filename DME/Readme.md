# DME - Connect

Dieses Script wird von User **paule3569** aus dem [Feuersoftware Forum](https://feuersoftware.com/forum/) eingesetzt um Alarme die ein [DME](https://de.wikipedia.org/wiki/Funkmeldeempf%C3%A4nger#Digitale_Meldeempf%C3%A4nger_(DME)) empfängt, auswertet und an die [Connect API](http://dokumentation.feuersoftware.com:8090/pages/viewpage.action?pageId=2490428) weiterleitet.

Besonderheit in dieser umsetzung ist es, das für jedes RIC ein eigener Token geladen wird.

- Thread: [Link](https://feuersoftware.com/forum/index.php?thread/2596-ansteuerung-der-schnittstelle-aus-textdatei/)
- Erklärung des Aufbaus durch paule3569: [Link](https://feuersoftware.com/forum/index.php?thread/2596-ansteuerung-der-schnittstelle-aus-textdatei/&postID=17141#post17141)

# Setup

Das Script läuft auf einem RaspberryPi 3 mit Raspian Stretch. (Andere Konfigurationen erfordern evtl. kleinere Änderungen)

Erst mal die notwendigen Pakete installieren
```
sudo apt-get install python3
sudo pip3 install requests pyserial coloredlogs
```

Nun das Script installieren
```
mkdir ~/connectapi
cd ~/connectapi
wget https://raw.githubusercontent.com/Bouni/ConnectAPI/master/DME/connectapi.py
sudo chmod +x connectapi.py
```
Die Tokens müssen in Dateien im Verzeichnis `~/connectapi` liegen und dem Namensschema `token_<ric>` folgen, also z.B. `token_01A`

Um das ganze als systemd Service laufen zu lassen, wie folgt vorgehen:

```
cd /etc/systemd/system
sudo wget https://raw.githubusercontent.com/Bouni/ConnectAPI/master/DME/connectapi.service
sudo systemctl daemon-reload
sudo systemctl enable connectapi.service
sudo systemctl start connectapi.service
```

Das Script erwartet den Melder an der Seriellen Schnittstelle `/dev/ttyS0`.

# Fehlerdiagnose

Fehlerdiagnose kann mit dem Befehl `journalctl -u connectapi.service -f` gemacht werden, dieser gibt das Logfile aus.

Das Script stoppen kann man mit `sudo systemctl stop connectapi.service`, danach kann man es zur besseren Fehlerdiagnose mit `~/connectapi/connectapi.py` ausführen um zu sehen wo es klemmt.
