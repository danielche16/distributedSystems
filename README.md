##  Verteilte Systeme WS21/22

## ANFORDERUNGSANALYSE

#### von Daniel Chenani und Leonie Zeiler


## Projektbeschreibung

### Aufgabenstellung

Im Rahmen des Praktikums Verteilte Systeme soll eine Anwendung aus dem Bereich der Logistik bzw.
Supply Chain Monitoring entwickelt werden. Dazu sollen die Technologien Sockets, Remote
Procedure Calls (RPCs) sowie Message-Oriented-Middleware (MOM) verwendet werden.

### Verwendete Tools

- Sprache: Python
- Formatierung: Json
- Build-Tool: Maven
- Deployment: Powershell


## Aufgabe 1a - UDP-Sockets

### Funktionale Anforderungen

Daten sollen über UDP-Sockets gesendet, empfangen und zugeordnet werden. Wenn Daten während des Sendevorgangs verloren gehen, dann soll der Empfänger das bemerken können.
Es kann beliebig viele unabhängige Lager mit dazugehörigen Sensor geben

### Nicht funktionale Anforderungen

Server und Sockets sollten dabei in der Lage sein immer unabhängig voneinander laufen zu können.

### Umsetzung

Simuliert wird ein Ein- und Ausliefern von Produkten und Inventarisation mit Hilfe der Sensoren. Dabei soll jeder der Sensoren ein eigenständiger Prozess sein. 
Die Informationen der Sensoren sollen sich kontinuierlich ändern und mit Hilfe von UDP permanent an das Lager geschickt werden. Das Lager gibt dann die empfangenen Pakete mit folgenden Informationen aus: IP, Sensor-Typ, Port. Diese Infos werden dann in einem Log-File gespeichert. 
Da es sich um den ersten Entwurf handelt und ein Proof of Concept ist, werden bestimmte Daten und deren Vollständigkeit außer Acht gelassen.

### Tests und Testumgebung

Es sollen mindestes 80% der Pakete erfolgreich und vollständig ankommen.
Die neuste Python-Version sollte immer installiert sein.


## Aufgabe 1b - TCP-Sockets

### Funktionale Anforderungen

Jedes Lager hat einen eigenen HTTP-Server, der mindestens einen HTTP-GET-Befehl korrekt und vollständig verarbeiten kann.
UDP- und TCP-Sockets sollen unabhängig voneinander laufen können und das Lager soll zur gleichen Zeit über UDP Pakete empfangen und über TCP mit HTTP-Clients in Kontakt bleiben können
Der HTTP-Server soll über verschiedene Routen die jeweiligen Daten zurückgeben können


## Aufgabe 2 - Remote Procedure Calls (RPC)

### Funktionale Anforderungen 

Die Lager sollen ihre Sensor-Daten über Thrift an andere Lager übermitteln können
Lager sollen Lieferungen simulieren können
Lager sollen abfragen können, welche Produkte sich in anderen Lagern befinden 

