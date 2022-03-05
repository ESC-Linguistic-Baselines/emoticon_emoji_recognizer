# Unicode Emoji und ASCII Emoticon Erkenner  
## Voraussetzungen
**Python 3.8+**
\
Das Programm wurde mit und für Python 3.8 geschrieben. Laden Sie die [aktuellste Version](https://www.python.org/downloads/) herunter und [installieren](https://docs.python.org/3/using/windows.html) sie.

**Python Module - Tweepy und Matplotlib**
\
Um auf Tweets von [Twitter](https://twitter.com/home) anhand einer API zugreifen zu können, wird das Modul [Tweepy](\https://www.tweepy.org/) benötigt. Es werden ebenfalls [API-Zugangsdaten](https://developer.twitter.com/en) gebraucht, die man bei Twitter beantragen kann. Diese Zugangsdaten müssen in der Datei *twitter_credentials.json* und entsprechend formatiert sein. 

Es werden  API-Zugangsdaten mitgeliefert, die temporär gültig sind. Wenn nötig, dürfen sie selbstverständlich gegen eigene Zugangsdaten ausgetauscht werden. Die Installation erfolgt ganz normal durch [pip](https://pypi.org/project/tweepy/).

Das  Programm kann ohne Tweepy und  die benötigten Zugangsdaten ausgeführt werden, aber der Zugriff auf Twitter und die zugehörigen Funktionen sind nicht funktionsfähig. 

Matplotlib muss ebenfalls via pip installiert werden, wenn man eine graphische bei der Auswertung der Zuverlässigkeit möchte. 

Das Programm kann ausgeführt werden, auch wenn die beide Module fehlen. 
Eine Stabilität des Programms kann jedoch nicht gewährleistet werden. 


**Emoticon/Emoji-Datenbank**
\
Die benötigten Basisdatenbanken werden dem Programm anhängend mitgeliefert.

## Beschreibung
Der Unicode Emoji und ASCII Emoticon Erkenner kann Textdateien sowie auch Tweets von [Twitter](https://twitter.com/) einlesen und die darin enthaltenen Emojis und Emoticons sowie auch deren Neubildungen erkennen und herausfiltern. 
Bei den Tweets gibt es die Möglichkeit entweder eine vorher selbst erstellte Datei mit Tweets einzulesen oder Suchparameter festzulegen, anhand dessen 10 Tweets von Twitter rausgesucht werden. Das Programm tokenisiert das Untersuchungsobjekt und anonymisiert alle Tweets, bevor es die Tokens in folgende Klassen unterteilt: *Nicht-Emoji-Emoticon*, *Emoji*, *Emoticon* und *Neubildung*.

###### **Weitere Funktionen:**
* Ergebnisauswertung *(Benötigt fertige Analyse)*
* Laufzeitberechnung des Programms
* Entleeren von Benutzerdatenbank und Ergebnisordner

## Benutzung 
#### Hauptmenü 

```
1: Textdatei auswerten
2: Tweet auswerten
3: Ergebnisauswertung
4: Laufdauerausgabe
5: Benutzeremoticon loeschen
6: Ergebnisse loeschen
7: Programminformation
8: Programm beenden
```

Nach Start des Programms landen Sie im Hauptmenü und können die einzelnen Menüpunkte über ihren Namen oder Ziffer anwählen, Groß- und Kleinschreibung spielen hierbei keine Rolle.

#### Auswählen des Untersuchungsobjekts
###### `1. Textdatei auswerten`
Es öffnet sich ein Dateimanagerfenster über das die zu untersuchende Datei ausgewählt werden kann.

###### `2. Tweet auswerten`
Sie werden zum Untermenü `Twitter Analyse` weitergeleitet, und können sich entscheiden ob Sie einen schon vorhanden Tweet Datei analysieren oder dynamisch Tweets von Twitter abrufen möchten.  
```
1: Text Tweet       # Öffnet ein Dateimanagerfenster zu Auswahl
2: Online Tweet     # Gibt Info aus und erfragt Input:

Sollen die Tweets auf 1. Englisch (ENG) oder 2. Deutsch (DE) sein: 1 
Geben Sie die Suchbegriffe nur von Leerzeichen getrennt an: Suchbegriff Suchbegriff
```
Nach Auswahl der Sprache der Tweets können bis zu 10 Suchbegriffe angegeben werden, jeweils von Leerzeichen getrennt. Die Suchbegriffe können entweder aus Hashtags wie *#hashtag* oder im Tweet vorhandenen Zeichenketten wie *:D* oder *Wort* bestehen. Es wird immer nach Tweets mit mindestens einer Übereinstimmung gesucht.

#### Datenbank
```
1: Programmdatenbank    
2: Benutzerdatenbank
```
Nach einlesen der zu untersuchenden Datei oder Tweets müssen Sie sich für eine Emoticon/Emoji Datenbank entscheiden. Entweder für die mitgelieferte Programmdatenbank oder eine schon vom Programm erstellte Benutzerdatenbank. Sollten Sie sich für die Benutzerdatenbank entscheiden, obwohl noch keine vorhanden ist, wird die Programmdatenbank kopiert. 

#### Abspeichern der Ergebnisse
```
1: Neue Emoticons übernehmen        # Ergebnisse abspeichern
2: Neue Emoticons verwerfen         # Ergebnisse löschen
3: Neue Emoticons/Emojis anzeigen   # Ausgabe der gefundenen Emoticons/Emojis
4: Alle Emoticons/Emojis anzeigen   # Ausgabe aller Emoticons/Emojis der Datenbank
5: Analyse Beenden                  # Zurück zum Hauptmenü
```
Nach Auswahl der Datenbank können Sie sich entscheiden was mit den Ergebnissen passiert. Bei Abspeichern der Ergebnisse können Sie sich entscheiden ob Alle oder nur bestimmte Zeilen übernommen werden sollen. Sobald Sie fertig sind können sie über `5. Analyse Beenden` zum Hauptmenü zurückkehren.

#### Ausgabe der Ergebnisse
```
1: Konsole                          # Nummerierte Ausgabe in die Konsole
2: Datei                            # Umnummeriertes Abspeichern in einer Datei
3: Konsole + Datei                  # Ausgabe und Abspeichern 
```
###### *Beispielausgabe*
```
1 @Benutzer_entfernt   Nicht_Emoji_Emoticon
2 Freunde              Nicht_Emoji_Emoticon
3 :)                   Standard-Emoticon
4 :-/                  Regex_Emoticon
5 😅                  Emoji
6 #Hashtag_entfernt    Nicht_Emoji_Emoticon
```
#### Weitere Funktionen
###### `3. Ergebnissauswertung`
```
1: .txt-Datei                         # TXT-Datei
2: .Xml Datei                         # XML-Datei
3: Beenden                            # Zurück zum Menü
```
Wählen Sie zunächst das Format der zu vergleichenden Datei aus. Anschließen öffnet sich erst ein Dateimanagerfenster zur Auswahl der Golddatei und danach eines zur Auswahl der Ergebnisdatei.
###### `4: Laufdauerausgabe`
```
1: Die Dauer des letzten Vorgangs      # Gibt die Zeit des letzten Durchgangs aus
2: Die Dauer aller Vorgaenge          # Gibt die Zeit aller Durchgänge seit Programmstart aus
3: Alle Zeiten löschen                # Löscht alle vorhandenen Zeiten aus dem internen Speicher
```
###### `5:  Benutzeremoticon loeschen`
Wählen Sie diesen Menüpunkt aus um die vom Programm erstellte Emoticon/Emoji Datenbank zu löschen.
\
*Es handelt sich hierbei nicht um die Programmdatenbank.*
###### `6: Ergebnisse loeschen`
Wählen Sie diesen Menüpunkt aus um alle Ergebnisdateien im Ergebnisordner zu löschen.
###### `7: Programminformation`
Wählen Sie diesen Menüpunkt aus um sich Informationen über das Programm ausgeben zu lassen.
###### `8: Programm beenden`
Wählen Sie diesen Menüpunkt aus um das Programm zu beenden.
## Autoren
Christopher Michael Chandler und Gianluca Cultraro 
