# FMS32Pro - Connect

Dieses Script wird von User **esche888** aus dem [Feuersoftware Forum](https://feuersoftware.com/forum/) eingesetzt um den Fahrzeugstatus der von FMS32Pro empfangen wird, über die [Connect API](http://dokumentation.feuersoftware.com:8090/pages/viewpage.action?pageId=2490428) zu setzen.

Thread: [Link](https://feuersoftware.com/forum/index.php?thread/2189-wunsch-tetracontrol-schnitstelle-für-fms32-verwenden/)

[FMS32Pro](https://www.heirue-soft.de/software/fms32) ist eine Windows Software, man kann das Python Script entweder auf dem selben Windows Rechner, oder auf einem anderen Linux Rechner laufen lassen.

# Setup unter Windows

Man installiert [Python](https://www.python.org/downloads/) in einer Version > 3.6. 
Wichtig ist das bei der Installation der Haken bei "Add Python to PATH" gesetzt ist.

Nun die notwendigen Pakete installieren, dazu ein CMD öffnen und folgendes eingeben:
```
pip install requests
```

Das Script wird an einen beliebeigen Ort gespeichert, z.B. C:\Programme\FMS32status\fms32status.py
Der Token muss in einen File Namens apitoken ohne Endung im selben Verzeichnis platziert werden.

Wir dieses dann z.B. von einem CMD aus gestartet `python  C:\Programme\FMS32status\fms32status.py` läuft das Script soweit.

Da ich keine Ahnung habe wie man unter Windows ein Script als Service einrichtet, warte ich darauf das jemand dafür eine Löung findet. 
Pull-Requests sind herzlich willkommen ;-)

# Setup unter Linux

Erst mal die notwendigen Pakete installieren
```
sudo apt-get install python3
sudo pip install requests
```

Nun das Script installieren
```
mkdir ~/fms32status
cd ~/fms32status
wget https://raw.githubusercontent.com/Bouni/ConnectAPI/master/FMS32/fms32status.py
```
Die Tokens müssen in Dateien im Verzeichnis `~/fms32status` liegen und den Namen `apitoken` haben.

Da das Script in diesem Fall auf einem anderen Rechner läuft als das FMS32Pro, muss die IP und der Port auf den des Rechners angepasst werden auf dem das FMS32Pro läuft:
```
class FMS32Pro:

    def __init__(self, ip='127.0.0.1', port=9300):
```

Um das ganze als systemd Service laufen zu lassen, wie folgt vorgehen:
```
cd /etc/systemd/system
sudo wget https://raw.githubusercontent.com/Bouni/ConnectAPI/master/FMS32/fms32status.service
sudo systemctl daemon-reload
sudo systemctl enable fms32status.service
sudo systemctl start fms32status.service
```

# Fehlerdiagnose

Fehlerdiagnose kann mit dem Befehl `journalctl -u fms32status.service -f` gemacht werden, dieser gibt das Logfile aus.
