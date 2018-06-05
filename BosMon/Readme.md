# BosMon - Connect

Dieses Script wird von User **marcosteeb** aus dem [Feuersoftware Forum](https://feuersoftware.com/forum/) eingesetzt um den Fahrzeugstatus der von BosMon empfangen wird, über die [Connect API](http://dokumentation.feuersoftware.com:8090/pages/viewpage.action?pageId=2490428) zu setzen.

Thread: [Link](https://feuersoftware.com/forum/index.php?thread/2189-wunsch-tetracontrol-schnitstelle-für-fms32-verwenden/)

[BosMon](https://www.bosmon.de/) ist eine Windows Software, man kann das Python Script entweder auf dem selben Windows Rechner, oder auf einem anderen Linux Rechner laufen lassen.

# Setup unter Windows

Man installiert [Python](https://www.python.org/downloads/) in einer Version > 3.6. 
Wichtig ist das bei der Installation der Haken bei "Add Python to PATH" gesetzt ist.

Nun die notwendigen Pakete installieren, dazu ein CMD öffnen und folgendes eingeben:
```
pip install requests
```

Das Script wird an einen beliebeigen Ort gespeichert, z.B. C:\Programme\bosmonstatus\bosmonstatus.py
Der Token muss in einen File Namens apitoken ohne Endung im selben Verzeichnis platziert werden.

Wir dieses dann z.B. von einem CMD aus gestartet `python C:\Programme\bosmonstatus\bosmonstatus.py` läuft das Script soweit.

Da ich keine Ahnung habe wie man unter Windows ein Script als Service einrichtet, warte ich darauf das jemand dafür eine Löung findet. 
Pull-Requests sind herzlich willkommen ;-)

# Setup unter Linux

Erst mal die notwendigen Pakete installieren
```
sudo apt-get install python3
sudo pip3 install requests
```

Nun das Script installieren
```
mkdir ~/bosmonstatus
cd ~/bosmonstatus
wget https://raw.githubusercontent.com/Bouni/ConnectAPI/master/BosMon/bosmonstatus.py
```
Der Token muss im Verzeichnis `~/bosmonstatus` liegen und den Namen `apitoken` haben.

Da das Script in diesem Fall auf einem anderen Rechner läuft als das BosMon, muss die IP auf '0.0.0.0' geändert werden und in BosMon dann die IP des Rechners als Ziel eingetragen werden:
```
if __name__ == "__main__":
    server = socketserver.TCPServer(("127.0.0.1", 5555), BosMonTCPHandler)
```

Um das ganze als systemd Service laufen zu lassen, wie folgt vorgehen:
```
cd /etc/systemd/system
sudo wget https://raw.githubusercontent.com/Bouni/ConnectAPI/master/BosMon/bosmonstatus.service
sudo systemctl daemon-reload
sudo systemctl enable bosmonstatus.service
sudo systemctl start bosmonstatus.service
```

# Fehlerdiagnose

Fehlerdiagnose kann mit dem Befehl `journalctl -u bosmonstatus.service -f` gemacht werden, dieser gibt das Logfile aus.
