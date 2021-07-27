# -*- coding: utf-8 -*-

'''
Erkenner von Unicode-Emojis und ASCII-Emoticons sowie entsprechender Neubildungen
Kurs: CL 1  - CL-Programmierung
Datum: 09/09/2020

# Christopher Michael Chandler                            # Gianluca Cultraro
# B.A, Romanische Philologie Franzoesisch und Linguistik  # B.A, Medienwissenschaft und Linguistik
# Romanische Philologie Franzoesisch B.A, 7. Semester     # Medienwissenschaft B.A, 8. Semester
# Linguistik B.A, 4. Semester                             # Linguistik B.A, 4. Semester
# Matrikelnummer: 108017107247                            # Matrikelnummer: 108014210767

'''

################ Importierung der notwendigen Module und Dateien ################


#########################
# Programmbeschreibung
#########################

'''

Die Hauptfunktion des Programms besteht darin einen Text in Bezug auf Emoticons und Emojis zu analysieren. 
Genauere Beschreibungen des Programms und dessen Funktonen befinden sich sowohl in der Dokumentation 
als auch in der Read-Me Datei. 

'''


#########################
# Importeriung der Standard Python Module
#########################

import csv, json, os, re, shutil
from subprocess import call
from time import perf_counter

#########################
# Ueberpruefung der Zusatzdateien
#########################

'''
Hier wird geprueft, ob die folgenden notwendigen Dateien vorhanden sind: 

emoji_datenbank.tsv - Datei, worin die Emojis gespeichert werden. 
emoticon_basisdatenbank.tsv - Datei, worin die Emoticons gespeichert werden. Anhand dessen werden die neuen Emoticons bestimmt.
nebenfunktionen.py - Nebenfunktionen z.B. Tokenizer, Tokenfilter, etc. die fuer die Ausfuehrung des Programms ausschlaggebend sind. 
'''

# Es muessen die drei Dateien vorhanden sein.
core_files_counter = 0  # Dateizaehler
missing_file = []  # Fehlende Dateie

# Liste der notwendigen Dateien
core_files = ["Ressourcen/Emoticons_emoji_datenbank/emoji_datenbank.tsv",
              "Ressourcen/Emoticons_emoji_datenbank/emoticon_basisdatenbank.tsv",
              "nebenfunktionen.py"]

# Mit einer For-schleife werden die Pfadnamen eingelesen.
for file in core_files:

    # Wenn die Datei existiert, wird der Zaehler um eins erhoert.
    if os.path.exists(file):
        core_files_counter += 1
    # Wenn eine Datei fehlt, wird sie hier gespeichert.
    else:
        missing_file.append(file)

# Wenn all Dateien vorhanden sind, wird core_files_available auf True gesetzt. Damit darf das Programm starten.
if core_files_counter == 3:
    core_files_available = True
else:
    # Wenn das nicht der Fall ist, wird das Programm nicht gestartet und die folgende Meldung wird angezeigt.
    core_files_available = False

    # Das Programm wird nicht ausgefuehrt, wenn die Zusatzdatei fehlt.
    print("Die folgenden Dateien fehlen oder der entsprechende (Pfad)Name wurde geaendert.\n")

    for file in core_files:
        # Wenn eine Datei vorhanden ist, wird die folgende Nachricht ausgegeben:
        if file not in missing_file:
            print(file, "(vorhanden)")
        else:
            # Wenn nicht, wird die folgende Nachricht ausgegeben.
            print(file, "(nicht vorhanden)")

    # Automatische Terminierung des Programms
    print("\nDa nicht alle Dateien wie vorgesehen vorhanden sind, wird das Hauptprogramm automatisch beendet.")
    raise SystemExit

#########################
# Importierung der Nebenfunktionen
#########################

# Wenn die wichtigen Dateien vorhanden sind, werden die notwendigen dann anschliessend Module importiert.
if core_files_available:

    # Falls Fehler bei der Importierung auftreten.
    try:

        '''
        Diese Funktionen befinden sich in der Datei nebenfunktionen.py.
        Sie sind essenziell fuer das Hauptprogramm. Ohne sie kann es nicht gestartet werden.
        Genauere Beschreibungen der einzelnen Funktionen befinden sich ebenfalls in der nebenfunktionen.py.
        '''

        # token_filter soll verhindern, dass der emoticon_emoji_erkenner Tokens faelscherweise als Emoticons taggt.
        # Tokenizer paarst und tokeniziert die Texte entsprechend.
        from nebenfunktionen import token_filter, tokenizer

        # Eine Datei via ein Tkdialogfenster aussuchen
        from nebenfunktionen import file_finder, information_window

        # Zusaetliche Funktionen, die im Hauptmenue ausgefuehrt werden.
        from nebenfunktionen import delete_user_emoticons, delete_result_folder

        # Funktionen zum Beenden des Programms und zur Ausgaben der Programminformationen
        from nebenfunktionen import program_information, program_end

        # Timer, womit die Analysedauer berechnet wird.
        from nebenfunktionen import time_analysis_menu

        # Ein Menue, das in den anderen Funktion eingesetzt wird.
        # idle_results liefert die Ergebnisse in tabellarischer Form.
        from nebenfunktionen import menu, idle_results

        # Eine Funktion, womit die Ergebnisse in tabellarischer Form im Ergebnisordner gespeichert werden.
        # Sie koennen auch im IDLE ausgegeben werden.
        from nebenfunktionen import output_results

        # Graphische Darstellung der Ergebnisse. Sie werden im Ergebnisordner gespeichert.
        from nebenfunktionen import bar_chart

        #########################
        # Importierung der Datenbanken aus der Nebenfunktionendatei
        #########################

        from nebenfunktionen import program_emoticon_database, user_emoticon_database, emoji_database
        from nebenfunktionen import emoticon_dict, emoji_dict

    # Falls es Probleme bei der Importierung der zugehoerigen Module gibt.
    except ImportError as error:
        print("Bei der Importierung einer Nebenfunktion ist ein Fehler aufgetreten:")
        print(f"\n{error}\n")
        print("Moeglicherweise liegt ein Tippfehler vor oder die zugehoerige Funktion ist nicht wie vorgesehen vorhanden. Bitte ueberpruefen Sie die Zusatzdatei.")
        print("\nDa nicht alle Dateien wie vorgesehen vorhanden sind, wird das Hauptprogramm automatisch beendet.")
        raise SystemExit  # Terminierung des Programms

#########################
# Importierung der Twittermodule
#########################

# tweepy muss via pip installiert werden.
# Es wird versucht, tweepy zu importiert.
try:
    import tweepy
except ImportError:
    # Wenn der Benutzer tweepy nicht schon vorher installiert hat, bekommt er eine Fehlermeldung.
    # Die Fehlermeldung wird hier ausgegeben.
    print(
        "\nDa das Modul 'tweepy' nicht installiert ist bzw. nicht importiert werden kann,\nkann das Programm nicht wie vorgesehen ausgefuehrt werden. ")

    while True:
        # Hier hat der Benutzer die Moeglichkeit das Programm trotzdem auszufuehren.
        program_continue = input("\nWollen Sie das Programm trotzdem ausfuehren? (y/n) " ).lower()

        # Zustimmung
        if program_continue == "y":
            # Das Programm wird ohne Tweepy ausgufuehrt.
            print("Die Weiternutzung des Programms ist eingeschraenkt, da 'tweepy' nicht vorhanden ist.")
            input("\nDruecken Sie die Eingabetaste, um fortzufahren: ")
            print()#Leerzeichen
            break

        # Ablehnung
        elif program_continue == "n":
            # Das Programm wird bei einer Verneinung nicht ausgefuehrt.
            print("Das Programm wird sofort beendet.")
            raise SystemExit

        # Unbekannte bzw. falsche Antwort
        else:
            print(f"{install} ist keine gueltige Antwort. Entweder 'y' oder 'n' eingeben.")


################ Das Hauptprogramm ################

#########################
# Hauptfunktionen
#########################

# Diese Funktion ist der dynamische Teil des Programms, da diese Funktion auf Tweets im Internet via tweepy zugreift.
def twitter_import():
    
    '''
    Die Offline Funktion fuer Twitter.
    Hier werden nur Tweets analysiert, die als .txt gespeichert abgespeichert sind.
    '''

    def text_tweet():
        # Die Datei wird mit der entsprechende Kodierung aufgemacht
        # file_finder() wird aufgerufen, damit der Benutzer sich die entsprechende Datei aussuchen kann.

        text=file_finder()
        #Wenn eine Datei vorhanden ist, wird es analysiert.
        if text:
            with open(text, mode="r", encoding="utf-8") as tweets:
                # Starten des Timers fuer die Laufzeitberechnung
                time_analysis(0)
                # Aufruf der Funktion zum Tokenisieren und Anonymisieren der Tweets
                tokens = tokenizer(tweets)
                # Beenden des Timers fuer die Laufzeitberechnung
                time_analysis(1)
        else:
            # Wenn eine Datei nicht vorhanden ist, wird eine Fehlermeldung gezeigt.
            # Dazu wird das Hauptmenue aufgerufen. 
            print("Es wurde keine Datei ausgewaehlt.")
            input("\nDruecken Sie die Eingabetaste, um wieder in das Twittermenu zu gelangen.")
            twitter_import()

        # Rueckgabewert der Tokens
        return tokens

    '''
    Die Online Funktion fuer die Twitter-API. 
    Hiermit werden tweets aus dem Internet heruntergeladen.
    Das Internet muss vorhanden sein, damit die Funktion ordnungsgemaess ausgefuehrt werden kann.  
    '''

    def online_tweets():
        # Verhindert einen Absturz des Programms, wenn kein Internet vorhanden ist.
        try:
            # Starten des Timers fuer die Laufzeitberechnung
            time_analysis(0)
            # Oeffnen der JSON Datei, die die Referenzen fuer Twitter beinhaltet
            with open("twitter_credentials.json", mode="r", encoding="utf-8") as file:
                creds = json.load(file)

            # Authentifizierung bei Twitter
            auth = tweepy.OAuthHandler(creds["API_KEY"], creds["API_SECRET"])
            auth.set_access_token(creds["ACCESS_TOKEN"], creds["ACCESS_SECRET"])

            # Erstellen des API-Objekts
            # wait_on_rate_limit = API goes auto wait, when limit reached, until it can start again
            # limit: 18k Tweets/15 min or 100 per request
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

            # Ueberpruefung ob die Authentifizierung erfolgreich war.
            # Je nach Ergebnis wird die Ausgabe des Authetifikationsstatusses definiert
            try:
                api.verify_credentials()
                auth_status = "Authentifizierung erfolgreich"
            except:
                auth_status = "Fehler bei der Authentifizierung"
            # Ausgabe des Authentifikationsstatusses
            print(auth_status)

            # Bei erfolgreicher Authentifizierung
            if auth_status == "Authentifizierung erfolgreich":
                # Ausgabe der Informationen ueber die Suchfunktion
                print(
                    f"########INFO########\n\nDie Suchfunktion gibt einen Mix der 10 neusten und populaersten Tweets aus.\n"
                    f"Sie koennen maximal 10 Suchbegriffe angeben.\nEs werden jedoch weniger empfohlen.\n"
                    f"Die Suchbegriffe koennen enthaltene Woerter oder #Hashtags sein.\nRetweets werden nicht gesucht um Duplikate zu verhindern.\n"
                    f"Es wird nach Tweets gesucht die mindestens einen Suchbegriff enthalten.\n")

                # Der Nutzer kann entscheiden ob die zu suchenden Tweets auf Englisch oder Deutsch sein sollen
                language = input("Sollen die Tweets auf 1. Englisch (ENG) oder 2. Deutsch (DE) sein:")
                # Diese Option wird als ISO 639-1 Code abgespeichert
                if language.title() == "1" or "Englisch" or "Eng":
                    slang = "en"
                elif language.title() == "2" or "Deutsch" or "De":
                    slang = "de"

                # Der User wird nach den Suchbegriffen gefragt
                search_query_inp = input("Geben Sie die Suchbegriffe nur von Leerzeichen getrennt an:")
                # Die Liste squery wird erstellt. Ihr werden die an den Leerstellen getrennte Suchbegriffe hinzugefuegt
                search_query = list()
                search_query.extend(search_query_inp.split())
                # Der String squery wird erstellt und ueber eine For-Schleife die Suchbegriffe + der Operator OR konkateniert
                squery = ""
                for sterm in search_query:
                    if sterm == search_query[-1]:
                        squery += sterm
                    else:
                        squery += sterm + " OR "
                # Der Filter Retweets wird dem String der Suchbegriffe konkateniert
                squery += " -filter:retweets"
                # Cursor Objekt wird erstellt. Die Twitter API wird angesteuert und such 10 Tweets.
                # Die Suche wird spezifiziert durch den Suchbegriff q= und die zu erkennende Sprache lang=
                tweets = tweepy.Cursor(api.search, q=squery, lang=slang).items(10)
                # Nur der Text der einzelnen Tweets aus dem Cursor Objekt wird der tweet_list hinzugefuegt
                tweet_list = [tweet.text for tweet in tweets]
                # Die Liste von Tweets wird an die twitter_anonymizer_tokenizer Funktion weitergeleitet
                tokens = tokenizer(tweet_list)

            # Beenden des Timers fuer die Laufzeitberechnung
            time_analysis(1)
            return tokens
        except:
            # Wenn Tweepy oder die Athentifizierung fehlschlagen, wird die folgende Information ausgegeben:
            error_message = "Da die Authentifizierung fehlgeschlagen ist, wird das Programm mit diesen Tokens fortgesetzt :) . "
            tokens = error_message.split()
            print(
                "\nDa die Authentifizierung fehlgeschlagen ist, wird das Programm mit den folgenden Beispieltokens fortgesetzt:\n")
            print(tokens)
            input("Druecken Sie die Eingabetaste, um fortzufahren: ")
            # Rueckgabe der Tokens
            return tokens

    # Funktionsmenue
    output_menu = {"Text Tweet": text_tweet,
                   "Online Tweet": online_tweets
                   }
    # Menu name
    menu_name = "Twitter Analyse"
    # Hinweise innerhalb des Menues
    menu_information = "Twitter Funktionen"
    # Das Menue wird aufgerufen.
    menu_results = menu(output_menu, menu_name, menu_information)
    return menu_results


'''
Mit dieser Funktion werden .txt-dateien Importiert. 
Anschliessend dann mit tokenizer tokenisiert. 
'''

def file_import(file):
    # Starten des Timers fuer die Laufzeitberechnung
    time_analysis(0)

    # Oeffnen der ausgewaehlten Datei
    with open(file, mode="r", encoding="utf-8") as text:
        # Erstellen der Tokenliste, indem tokenizer aufgerufen wird.
        tokens = tokenizer(text)
    time_analysis(1)
    # Rueckgabewert der Tokens
    return tokens


'''
Diese Funktion soll drei Arten von Tokens erkennen:
Emoticons sowohl rueckwarts als auch vorwaerts, die sich aus ASCII-Zeichen zusammensetzten
Emojis, die per Unicode im Vorfeld festgelegt und definiert wurden.
Neubildung, die sich aus ASCII-Zeichen und eventuell Emojis zusammensetzen. 
'''

def emoticon_emoji_erkenner(tokens):
    # Starten des Timers fuer die Laufzeitberechnung
    time_analysis(0)

    # Emoticon Dictionary und die getaggten Ergebnisse als Dictionaries
    result_dict, regex_emoticons_dict = dict(), dict()

    #########################
    # Emoticon Datenbank
    #########################

    '''
    Es werden zwei separaten Datenbanken angeboten: die Basisdatenbank und die Benutzerdatenbank.
    Die Programmdatenbank wird mitgeliefert und ist somit statisch.
    Die Benutzerdatenbank ist eine Kopie der Programmdatenbank und plus die Emoticons gewonnen aus der Analysen
    Das heisst, dass die Benutzerdatenbank mit jeder Analyse waechst bzw. wachsen kann, wenn der Benutzer das so moechte. 
    '''

    # Es wird geprueft, ob eine Benutzerdatenbank vorhanden ist.
    # Wenn nicht, wird eine Kopie der Programmdatenbank erstellt, woraus eine Benutzerdatenbank erstellt wird.
    if os.path.exists(user_emoticon_database) is not True:
        # Es wird eine Kopie der Programmdatenbank erstellt, woran die neuen Emoticons angehangen werden.
        shutil.copy(program_emoticon_database, user_emoticon_database)

    # Die Emoticondatenbank des Programms
    def program_database():
        # Wiedergabe der Datenbank
        return program_emoticon_database

    # Die Emoticondatenbank des Benutzers
    def user_database():
        # Wiedergabe der Datenbank
        return user_emoticon_database

    # Beenden des Timers fuer die Laufzeitberechnung
    time_analysis(1)

    # Beide Funktion werden in output_menu gespeichert.
    output_menu = {"Basisdatenbank": program_database,
                   "Benutzerdatenbank": user_database
                   }

    # Hier wird das Menue aufgerufen. Die Wahl des Benutzer wird als Variabel gespeichert.
    menu_information = "Welche Datenbank moechten Sie fuer die Auswertung benutzen ?"
    database = menu(output_menu, "Datenbank", menu_information)

    #########################
    # Einlesung der Datenbank
    #########################

    '''
    Hinweis zur Aufbau der Emoticons:

    Ein Emoticon, sowie es im Programm gehandhabt wird, besteht aus drei Hauptkomponenten: Head, Body und Tail.
    Head ist der Kopf des Emoticons, der aus einem Zeichen besteht.
    Body bildet den Koerper des Emoticons. Dieser kann beliebig lang sein, aber befindet sich immer zwischen Head und Tail.
    Tail ist das letzte Zeichen, das nach Body erfolgt.
    '''
    # Starten des Timers fuer die Laufzeitberechnung
    time_analysis(0)

    # Die ausgewaehle Emoticondatenbank wird mit dem modus r und der Enkodierung utf-8 eingelesen.:
    with open(database, mode="r", encoding="utf-8") as emoticons:
        # Mengen fuer die entsprechenden Emoticon head, body, tail
        head_set, body_set, tail_set = set(), set(), set()

        # Mit einer For-schleife werden die Emoticons eingelesen.
        for row in emoticons:
            # Das tatsaechliche Emoticon wird hier erfasst.
            emoticon = row.split()[0]
            # Der Emoticonname wird hier erfasst.
            emoticon_name = row.split()[1]
            # Sowohl Emoticon als auch dessen Namen werden in einem Dictionary gespeichert.
            emoticon_dict[emoticon] = emoticon_name

            # Emoticonkomponente
            head = row.split()[0][0]  # Kopf
            body = row.split()[0][1:len(row.split()[0]) - 1]  # Body

            # Komplexe Emoticons sind die Emoticons, die mehr als 3 Zeichen haben.
            if len(emoticon) >= 3:
                # Das erste Zeichen wird an head_set angehangen.
                head_set.add(head)
                # Alle Zeichen zwischen head und tail werden an body angehangen.
                # Der Body muss erstmals zerlegt werden, da es aus mehreren einzelnen Zeichen besteht.
                for element in sorted(body):
                    body_set.add(element)
                # Das letzte Zeichen wird an Tail angehangen.
                tail_set.add(row.split()[0][-1:])
            # Einfache Emoticons sind alle Emoticons, die genau zwei Zeichen haben.
            elif len(emoticon) == 2:
                head_set.add(row.split()[0][0])
                body_set.add(row.split()[0][1])
                # Hier ist kein Tail. Es wird angenommen(naiv), dass der Body als Body und als Ende gleichzeitig fungiert.
        '''
        Anmerkung: 

        Es wird in dem Programm davon ausgegangen, dass ein Emoticon zwar beliebig lang sein kann, jedoch nicht beliebig kurz. 
        Aufgrund dessen darf bzw. kann ein Emoticon nicht kleiner als zwei Zeichen sein, da mindestens zwei Zeichen noetig sind,
        um eine sinnvolle Bildhaftigkeit zu erzeugen. 

        '''

        #########################
        # Regex
        #########################

        # Erstellung der entsprechenden Zeichnungsklassen fuer die Regulaere Ausdruecke.

        # Offene Klammer der RA
        head, body, tail = "[", "[", "["
        # Anhand die For-Schleifen werden die Zeichenklassen automatisch gefuellt.
        for element in sorted(head_set): head += element  # Kopf
        for element in sorted(body_set): body += element  # Body
        for element in sorted(tail_set): tail += element  # Tail
        # geschlossene Klammer der jeweiligen RA
        head += "]"
        body += "]"
        tail += "]"

        # Regulaere Ausdruecke, womit neue Emoticons erkannt werden.
        new_emoticon = re.compile(rf"{head}{body}+{tail}*")

        '''
        Anhand einer For-schleife wird es nach drei Arten von Emoticons gesucht:
        Emoticons, die sich im Basiskorpus befinden, :P (Emoticons)
        Emoticons, die sich im Basiskorpus, aber rueckwaerts. P: (Emoticons)
        Emoticons, die nach dem oben definierten regulaeren Ausdruecke gefunden bestimmt wurden. :-/ (Neubildungen)
        '''

        #########################
        # Bestimmung der Emoticons und Emojis
        #########################

        # Ein Emoticon (vorwaerts), das sich in der Datenbank befindet.
        for number, token in enumerate(tokens):
            # Wenn das Emoticon vorhanden ist, wird das Dictionary entsprechend ergaenzt.
            if token in emoticon_dict:  # Emoticons
                result_dict[(number, token)] = "Emoticon"
            elif token in emoji_dict:  # Emojis
                # res_dict wird dadurch ergaentzt.
                result_dict[(number, token)] = "Emoji"
            for res in emoticon_dict:  # Emoticon rueckwarts
                if token == res[::-1]:
                    # res_dict wird dadurch ergaentzt.
                    result_dict[(number, token)] = "Emoticon"

            token_filter_tag = token_filter([token])[0][1]
            # Wenn ein Emoticon bestimmt wird, wird es in dem result_dict gespeichert wie folgt: ":)" : Tag
            '''
                 Hier wird token_filter aufgerufen. 
                 
                 Da man die gleichen Zeichen fuer Woerter und fuer Emoticons benutzen kann,
                 kann es vorkommen, dass ein Wort faelscherweise als Emoticon bzw. Neubildung getaggt wird. 
                 Um dies zu vermeiden, werden die Tokens vorher sortiert und entsprechend getaggt. 
                 Alle Tokens, die den Tag potenzielles_emoticon haben, werden weiter untersucht. 
                 Die anderen Tags sind allerdings nicht weiter von Belangen fuer den weiteren Verlauf des Programms.
                '''
            if token_filter_tag == "potenzielles_emoticon":
                # Regexemoticons, die von dem regulaeren Ausdruck erkannt wurden und nicht im Emoticon_dict vorhanden sind.
                if new_emoticon.match(token) and token not in emoticon_dict and token[0] != token[1]:
                    # result_dict wird dadurch ergaentzt.
                    result_dict[(number, token)] = "Neubildung"
                    # regex_emoticon_dict
                    regex_emoticons_dict[(number, token)] = "Neubildung"
            # Alle andere potenziellen Emoticons werden als Rest eingestuft.
            elif token not in result_dict:
                result_dict[(number, token)] = "Rest"

            # Alle Tokens, die uebrig bleiben, werden als Rest eingestuft.
            elif token not in result_dict:
                result_dict[(number, token)] = "Rest"

        #########################
        # Ergebnisse speichern
        #########################
        '''
        Um das Programm zu trainieren, wird eine separate Datei zur Verfuegung gestellt.
        Wenn man das Programm "falsch" trainiert hat, kann man sich immer noch auf den Basiskorpus beziehen.
        '''

        # Die Ergebnisse werden beibehalten.
        def accept_results():
            # Die Ergebnisse der Benutzerdatenbank werden in dieser Liste gespeichert.
            emoticon_database_list = list()
            # Die Emoticons des Benutzers werden hiermit eingelesen
            with open(user_emoticon_database, mode="r", encoding="utf-8") as emoticon_text:
                # Ein CSV_reader mit einem Tabulator wird erzeugt.
                emoticon_text_reader = csv.reader(emoticon_text, delimiter="\t")
                # Die emoticon_database_list wird durch die Emoticons ergaenzt.
                for emoticon in emoticon_text_reader:
                    # Es wird immer die erste Spalte bzw. Spalte 0 genommen, da die Emoticons dort gespeichert sind.
                    emoticon_database_list.extend(emoticon[0])

            # Die Ergebnisse werden in einer separaten Datei gespeichert.
            with open(user_emoticon_database, mode="a", encoding="utf-8") as user_emoticons:
                # Die Emoticons werden in einer Set gespeichert, damit die Duplikaten aussortiert werden auftreten.
                regex_set = set()
                # Es wird nur das erste Element entnommen, da das nullte Element die Nummerierung ist.
                for key in regex_emoticons_dict: regex_set.add(key[1])

                # Der Benutzer kann alle Ergebnisse uebernehmen oder nur bestimmte Teile davon.
                regex_choice = input("Welche Zeilen moechten Sie uebernehmen: alle (1) / bestimmte Zeilen (2) ?")

                # Alle Ergebnisse wieder hiermit uebernommen bei einer Zustimmung.
                if regex_choice == "1":
                    # Mit enumerate koennen die Zeilen bestimmt werden. Die Nummerierung faengt bei 1 an.
                    for line, element in enumerate(tuple(regex_set), start=1):
                        # Wenn das Emoticon in der Datenbank schon vorhanden ist, wird es nicht uebernommen.
                        # Somit kann man Dubletten in der Benutzerdatenbank vermeiden.
                        if element not in emoticon_database_list:
                            # Ergaenzung der Datenbank
                            user_emoticons.write("\n" + element + "\t" + "Neubildung")
                    # Der Vorgang wurde erfolgreich abgeschlossen.
                    print("\nDie Ergebnisse wurden uebernommen.\n")

                # Nur bestimmte Ergebnisse werden uebernommen.
                elif regex_choice == "2":
                    # Die Zeilenangaben des Benutzers
                    regex_choice_set = set()

                    # Der Benutzer soll die Zeilen eingeben, die uebernommen werden sollen.
                    regex_choice_2 = input("Geben Sie die Zeilennummer getrennt durch Leerzeichen an: ")

                    # Die Ziffern werden in einer Set gespeichert, damit die Dubletten entfernt werden.
                    for number in regex_choice_2.split(): regex_choice_set.add(number)  # Ergaenzung der Menge

                    # Hier werden nur bestimmte Emoticons uebernommen.
                    for line, element in enumerate(tuple(regex_set), start=1):
                        # Wenn die Zeile in der Menge vorhanden ist und das Emoticon ist nicht in der Menge, wird das Emoticon uebernommen.
                        if str(line) in regex_choice_set and element not in emoticon_database_list:
                            # Ergaenzung der Datenbank
                            user_emoticons.write("\n" + element + "\t" + "Neubildung")
                    # Ergebnisse, die spaeter uebernommen werden.
                    print("\nDie Ergebnisse wurden uebernommen.\n")

        # Die Ergebnisse werden verworfen und nicht in die Datenbank mitaufgenommen.
        def reject_results():
            # Der Benutzer wird darauf hingewiesen, dass verworfene Emoticons nicht wiederhergestellt werden koennen.
            print("\n⚠️ Verworfene Emoticons koennen nicht wiederhergestellt werden ⚠️\n")
            final_answer = input("Sind Sie sich sicher? (Y/N)").lower()

            # Der Benutzer soll angegeben, ob die Ergebnisse wirklich verworfen werden sollen.
            while True:
                # Der Benutzer erfaehrt, dass die Ergebnisse geloescht wurden.

                # Zustimmung
                if final_answer == "y":
                    print("\nDie Ergebnisse wurden verworfen.\n")
                    # Abbruch der While-Schleife
                    break

                # Ablehnung
                elif final_answer == "n":
                    # Abbruch der While-Schleife
                    print("\nDie Ergebnisse wurden nicht verworfen.\n")
                    break
                # Falsche oder unbekannte Antwort
                else:
                    print(f"{final_answer} ist keine gueltige Anwort")

        # Die Ergebnisse werden zwar angezeigt, aber nirgendwo gespeichert.
        def display_all_results():
            print("Alle - Emoticon und Emoji Ergebnisse:\n")
            # Eine separate Funktion wird aufgerufen, um die Ergebnisse ordentlich in der Konsole wiederzugeben.
            emoticon_results_dict = dict()

            # Das Emoticon_results Dictionary wird mit einer for-schleife gefuellt.
            for key in result_dict:
                # Alles, was nicht ein Emoji oder Emoticon ist,  wird nicht hier angezeigt.
                if "Rest" != result_dict[key]:
                    emoticon_results_dict[key] = result_dict[key]
            # Wenn es nicht nicht leer ist, werden die Ergebnisse angezeigt.
            if emoticon_results_dict:
                # Ergebnisfunktion wird aufgerufen.
                idle_results(emoticon_results_dict)
                input("Druecken Sie die Eingabetaste, um fortzufahren: ")
            else:
                # Wenn sie nicht vorhanden sind, bekommt der Benutzer die folgende Meldung:
                print("Es gibt keine Emoticons in diesem Text.")
                # Informationsfluss kontrollieren
                input("Druecken Sie die Eingabetaste, um fortzufahren: ")

        def display_new_results():
            # Wenn Regex emoticons vorhanden sind, werden sie angezeigt.
            if regex_emoticons_dict:
                # Nur neue Emoticons bzw. Neubildungen werden angezeigt.
                print("Neue - Emoticon und Emoji Ergebnisse:\n")
                # Ergebnissfunktion wird aufgerufen.
                idle_results(regex_emoticons_dict)
                input("Druecken Sie die Eingabetaste, um fortzufahren: ")
            else:
                # Wenn sie nicht vorhanden sind, bekommt der Benutzer die folgende Meldung.
                print("Es gibt keine neuen Emoticons bzw. Neubildungen in diesem Text.")
                # Informationsfluss kontrollieren.
                input("Druecken Sie die Eingabetaste, um fortzufahren: ")

        # Abbruchfunktion innerhalb des Menues
        def finish():
            # Wenn diese Funktion ausgefuehrt wird, wird choice auf Falsch gesetzt und somit ist die Funktion beendet.
            choice = False
            return choice

            # Beenden des Timers fuer die Laufzeitberechnung
            time_analysis(1)

        # Hier wird der Benutzer aufgefordert, entweder die neuen Emoticons zu speichern oder zu verwerfen.
        output_menu = {"Neue Emoticons uebernehmen": accept_results,
                       "Neue Emoticons verwerfen": reject_results,
                       "Neue Emoticons/Emojis anzeigen": display_new_results,
                       "Alle Emoticons/Emojis anzeigen": display_all_results,
                       "Analyse Beenden": finish()
                       }
        menu_information = "Wie moechten Sie mit den Ergebnissen verfahren ?\nHinweis: Der Basiskorpus bleibt von Aenderungen grundsaetzlich unberuehrt.\n"

        # Die While-Schleife bleibt solange bestehen bis der Benutzer sie mit finish beendet hat.
        choice = True
        while choice:
            # Das Menu wird ausgefuehrt.
            res = menu(output_menu, "Ergebnisse", menu_information)
            if res is False: break

    # result_dict sind alle Emoticons (regex auch), die im Text gefunden wurden.
    return result_dict


'''
Mit dieser Funktion kann man die Zuverlaessigkeit des Programms bestimmen. 
Es werden zwei Dateien gleicher Laenge bzw. Anzahl an Tokens benoetigt. 
Eine Golddatei, worin die korrekte Zuordnung der Tokens gespeichert sind und eine zugehoerige Ergebnisdatei. 
Diese werden miteinander verglichen und man bekommt am Ende eine Auswertung der Uebereinstimmung der beiden Texte. 
'''


def reliability_analysis():
    # Boolesche Wert, um die Choice-Schleife zu brechen.
    choice = True

    # Zwei Textdateien_training, wobei eine als Referenztext (gold) wogegen ein Ergebnisdatei verglichen wird.
    def gold_file():
        # Golddatei
        #Ein Tkfenster wird erzeugt
        information_window("Bitte waehlen Sie die Golddatei aus.")
        gold = file_finder()
        # Ergebnisdatei
        #Ein Tkfenster wird erzeugt
        information_window("Bitte waehlen Sie die Ergebnisdatei aus.")
        result = file_finder()

        # Beide Dateien mit der entsprechenden Kodierung werden aufgemacht.
        with open(gold, mode="r", encoding="utf-8") as gold_tags, open(result, mode="r",
                                                                       encoding="utf-8") as result_tags:
            # Anzahl der folgenden Tags
            # Falsche Tags: ein falscher Tag liegt vor, wenn der Ergebnistag vom Goldtag abweicht.
            # Emoticons, die im Text vorkommen.
            # Emojis, die im Text vorkommen.
            # Neubildungen, die durch den regulaeren Ausdruck bestimmt wurden.
            incorrect_tags, emoticons, emojis, regex_emoticons, rest = 0, 0, 0, 0, 0

            # Hier werden alle Tokens und Tags von beiden Dateien gespeichert.
            tag_dict = dict()

            # Mit zip werden beide Dateien parallel ausgegeben.
            # Enumerate zaehlt die Tags und die letzte Enumerate-Zahl entspricht der Anzahl der Tags.
            for tag_line, (line_one, line_two) in enumerate(zip(gold_tags, result_tags)):
                # Der Schluessel ist ein Token und Werte sind die Tags (Standard, Golddateien_training)
                tag_dict[tag_line, line_one.split()[0]] = (line_one.split()[1] + "\t\t" + line_two.split()[1])

                # Die folgenden Zaehler werden entsprechend erhoeht, wenn die Bedingungen vorliegen.
                if line_two.split()[1] == "Emoticon":
                    emoticons += 1  # Emoticons
                elif line_two.split()[1] == "Emoji":
                    emojis += 1  # Emojis
                elif line_two.split()[1] == "Neubildung":
                    regex_emoticons += 1  # Neubildungen
                elif line_two.split()[1] == "Rest":
                    rest += 1  # Rest

                # Wenn beide Tags abweichen, liegt ein Fehler vor. Dies wird als ein "falscher Tag" eingestuft.
                if line_one.split()[1] != line_two.split()[1]: incorrect_tags += 1

            # Diese Werte werden zuerst auf 0 gesetzt, aber spaeter durch die entsprechenden Werte ersetzt.
            # Fehlerrate als Prozentzahl, Uebereinstimmung der beiden Texte als Prozentzahl
            error_percentage, match = 0, 0

            # Information in Bezug auf Taganzahl, Uebereinstimmung der beiden Texte und alle Tokens mit deren Tags.
            reliability_dict = {"Anzahl saemtlicher Tags": tag_line,  # Anzahl der Emoticons
                                "Anzahl falscher Tags": incorrect_tags,  # Falsche Tags
                                "uebereinstimmung": match,  # Aehnlichkeit der beiden Texte
                                "Fehlerrate": error_percentage,  # Fehlerrate der beiden Texte
                                "Token": "Goldtag\t\tProgrammtag"
                                }  # Tokens in der Ergebnisdatei

            # Realiabitiy_dict wird durch die tags und Tokens ergaenzt.
            # Damit alles in einer einzigen Datei gespeichert werden kann.
            for tag in tag_dict:
                reliability_dict[tag] = tag_dict[tag]

            # Fehlerrate als Prozentzahl z.B. 2%
            error_percentage = round(100 * float(incorrect_tags) / float(tag_line), 2)
            reliability_dict["Fehlerrate"] = error_percentage

            # Uebereinstimmung der beiden Texte als Prozentzahl z.B. 70% Uebereinstimmung
            match = 100 - round(100 * float(incorrect_tags) / float(tag_line), 2)
            reliability_dict["uebereinstimmung"] = match

            # Output_results wird aufgerufen und reliability dict wird dann als Ergebnisdatei gespeichert.
            output_results(reliability_dict, rel_has_run=True)
            # Werte fuer die Erzeugung der Balken
            values = [emoticons, emojis, regex_emoticons, rest]

            # Graphische Ergebnisse
            bar_chart(values)

    '''
    Von dem Dortmund Chatkorpus werden XML-Dateien als annotierte Loesungen geliefert. 
    Aufgrund dessen funktioniert diese Auswertung anders. Es wird geschaut, wie viele Emoticons in dem Programm auftauchen. 
    Sie werden in der XML-Datei wie folgt markiert z.B. <emoticon>:)</emoticon>.
    Dann wird in der Ergebnisdatei geschaut, ob dieses Emoticon auftaucht und ob sie von unserem Programm als Emoticon richtig getaggt wurde. 
    Emojis tauchen in diesen Dateien grundsaetzlich nicht auf und sind somit irrelevant fuer die Auswertung.
    '''

    def xml_file():
        # Regulaere Ausdruck, womit die Emoticons aus der XML-Datei erkannt werden.
        xml_emoticon = re.compile(r"<emoticon>(.+)</emoticon>$")

        # Alle Emoticons aus der Golddatei werden hier gespeichert.
        xml_emoticon_set = set()

        # Hier werden die Emoticons und Tags aus der entsprechenden Ergebnisdatei gespeichert.
        result_file_dict = dict()

        # Golddatei
        information_window("Bitte waehlen Sie die Golddatei mit dem .XML format aus.")
        gold = file_finder()

        # Ergebnisdatei
        information_window("Bitte waehlen Sie die Ergebnisdatei aus.")
        result = file_finder()

        # Beide Dateien werden mit der entsprechenden Kodierung aufgemacht.
        # Da es Probleme bei der Einlesungen von XML-Dateien geben kann, werden sie mit "ignore" ignoriert.
        with open(gold, mode="r", encoding="utf-8", errors="ignore") as xml_file, \
                open(result, mode="r", encoding="utf-8", errors="ignore") as results_file:

            # Die XML-Datei wird eingelesen.
            for line in xml_file.read().split():
                if xml_emoticon.findall(line):
                    # wird es in dem xml_emoticon Dictionary gespeichert.
                    xml_emoticon_set.add(xml_emoticon.findall(line)[0])

            # Die Ergebnisdatei wird mit einer For-Schleife aufgemacht.
            for row_number, line in enumerate(results_file):
                # Die Datei wird in zwei Spalten getrennt: Emoticon und Tag
                emoticon, tag = line.split()[0], line.split()[1]

                # Nicht-Emoticons werden von der Datei ausgeschlossen.
                # if tag != "Emoticon":
                # Diese Emoticons werden mit in die Analyse aufgenommen.
                result_file_dict[row_number, emoticon] = tag
                # Dadurch wird das entsprechende Dictionary ergaenzt
        '''
        Diese Werte werden zuerst auf 0 gesetzt, aber spaeter durch die entsprechenden Werte ersetzt. 
        '''

        # Anzahl der falschen Tags, uebereinstimmung der beiden Texte,  Fehlerrate als Prozentzahl
        incorrect_tags, match, error_percentage = 0, 0, 0

        # Information in Bezug auf Taganzahl, Uebereinstimmung der beiden Texte und alle Tokens mit deren Tags.
        reliability_dict = {"Anzahl an Emoticons": len(result_file_dict),  # Anzahl der Emoticons
                            "Anzahl falscher Tags": incorrect_tags,  # Falsche Tags
                            "uebereinstimmung": match,  # Aehnlichkeit der beiden Texte
                            "Fehlerrate": error_percentage,  # Fehlerrate der beiden Texte
                            "Token": "Programmtag\t\tGoldtag"
                            }  # Tokens in der Ergebnisdatei

        # Hier werden das Ergebnis-Dictionary und die Emoticon-menge aus der XML-Datei miteinander verglichen.
        for tag_line, key in enumerate(result_file_dict):

            # Wenn das Emoticon aus dem Ergebnis-Dictionary in der Menge vorhanden ist
            if key[1] in xml_emoticon_set:
                # gilt dies dann als richtig und wird entsprechend aufgenommen.
                reliability_dict[tag_line, key[1]] = result_file_dict[key] + "\t" + "Emoticon"
            else:
                # Falls es nicht vorhanden ist, wird der Zaehler um eins erhoeht.
                incorrect_tags += 1
                # Das reliability_dict wird durch den Key, dessen Wert ergaenzt.
                reliability_dict[tag_line, key[1]] = result_file_dict[key] + "\t" + "Nicht Vorhanden"
        # Ersetzung der oben festgelegten Variablen
        reliability_dict["Anzahl falscher Tags"] = incorrect_tags  # Falsche Tags
        reliability_dict["uebereinstimmung"] = round(100 * float(incorrect_tags) / float(len(result_file_dict)),
                                                     2)  # Uebereinstimmung
        reliability_dict["Fehlerrate"] = 100 - round(100 * float(incorrect_tags) / float(len(result_file_dict)),
                                                     2)  # Fehlerrate
        # Ausgabe der Ergebnisse
        output_results(reliability_dict, rel_has_run=True)

    # Hiermit kann man die Choice-Schleife brechen.
    def finish():
        # Choice wird auf falsch gesetzt von innerhalb des Menues.
        choice = False
        return choice

    # Menueinformationen
    output_menu = {".txt Datei": gold_file,
                   ".XML Datei": xml_file,
                   "Beenden": finish(),
                   }
    menu_name = '\nErgebnisauswertung\n'  # Menuename
    menu_information = 'Hier koennen Sie bestimmen wie weit Ihre Ergebnisse von den Goldtags abweichen\n'  # Menueinformation

    while choice:  # Choice-Schleife
        res = menu(output_menu, menu_name, menu_information)
        # Wenn der Benutzt sich finish aussucht, wird die Schleife gebrochen.
        if res == False: break


# Timer mit Start und Stop und Stopfunktion
# Ein Aufrufen der Datei mit einem Wert dessen boolscher Wert False ist (wie O) startet den Timer
# Ein erneutes Aufrufen mit einem Wert dessen boolscher Wert True ist (wie 1) beendet den Timer
def time_analysis(end):
    if not end:
        # global statement, da die Function fuer den End Timer erneut aufgerufen wird
        global start_time
        # Initialisieren des Timers
        start_time = perf_counter()

    if end:
        # Feststellen der Endzeit
        end_time = perf_counter()
        # Berechnen der gebrauchten Zeit
        times = end_time - start_time
        # Die Zeiten der Functionslaeufe werden der Liste running_time hinzugefuegt
        running_time.append(times)


################ Aufruffunkion des Hauptprogramms und der zugehoerigen Funktionen ################

# Run_programm hat nur die Funktion, die oben genannten Funktionen ausfuehren. Somit dient es als Hauptmenue des Programms.
def run_program():
    # Auf der Oberflaeche koennen die Funktionen entweder mit der entsprechenden Ziffer oder mit dem entsprechenden Namen ausgefuehrt werden.
    menu_option = {"Textdatei auswerten": file_import,
                   "Tweet auswerten": twitter_import,
                   "Ergebnisauswertung": reliability_analysis,
                   "Laufdauerausgabe": time_analysis_menu,
                   "Benutzeremoticon loeschen": delete_user_emoticons,
                   "Ergebnisse loeschen": delete_result_folder,
                   "Programminformation": program_information,
                   "Programm beenden": program_end
                   }

    # Fehlermeldung bei einer ungueltigen Eingabe. D.h. eine Eingabe, die sich nicht in dem Dictionary menu_option befindet.
    invalid_option = "Leider ist ein Fehler aufgetreten. Mit der Eingabetaste gelangen Sie wieder in das Hauptmenue"

    # Die Schleife bleibt solange bestehen, bis es durch programm_beenenden gebrochen wird.
    while True:
        # Eingebettete While-Schleife damit, das Hauptmenue wieder aufgerufen werden kann.
        while True:
            banner = "\t\t~ Emoticon und Emoji Erkenner Version 1.0 ~ ", "\t\t\t\t#### Hauptmenue ####"
            for word in banner: print(word)
            print("\n- Gross- und Kleinschreibung muessen nicht bei der Eingabe beruecksichtigt werden- \n")
            # Mit einer For-Schleife wird das Hauptmenue angezeigt. Die Nummerierung faengt bei 1 an.
            for num, elem in enumerate(menu_option, start=1):
                print(f'{num}: {elem}')
            # Der Benutzer wird aufgefordert sich eine Funktion ausgesucht.
            choice_str = input('\nBitte die Nummer des Menuepunkts oder dessen Namen eingeben: ').strip()
            # Die entsprechende Funktion wird von menu_option entnommen und ausgefuehrt.
            options_func_dict = menu_option.get(choice_str.title())
            # Wenn die Eingabe sich mit einer Funktion in dem Dictionary uebereinstimmt, wird die Schleife gebrochen.
            if options_func_dict:
                break
            # Es wird geprueft, ob der Benutzer eine Ziffer eingegeben hat.
            else:
                try:
                    # Die Funktion nummerisch aufrufen.
                    choice_num = int(choice_str)
                except:
                    # Der Benutzer wird darauf hingewiesen, dass die Eingabe ungueltig ist.
                    input(invalid_option)
                else:
                    #Wenn aber die Funktion gueltig ist, wird es aufgerufen
                    if 0 < choice_num and choice_num <= len(menu_option):
                        #Die Werte (Funktionen) des Dictionarys werden als Liste gespeichert.
                        func_list=list(menu_option.values())
                        # Es wird aus dieser Liste die Funktion per Indizierung gezogen.
                        function_number=choice_num - 1
                        # Die Funktion
                        options_func_dict = func_list[function_number]
                        # Die Funktion wird weitergegben.
                        # Die Schleife wird gebrochen.
                        break
                    else:
                        # Der Benutzer wird darauf hingewiesen, dass die Eingabe ungueltig ist.
                        input(invalid_option)

        # Wenn Text File Analysis oder der zweite Menuepunkt ausgesucht wurde,
        # wird sie von anders ausgefuehrt, da ein Argument erforderlich ist.
        if "file_import" in str(options_func_dict):

            # Hier wird der Benutzer per Dialogfenster aufgefordert, sich eine Datei aussuchen.
            # Es spielt dabei keine Rolle, wo die Datei sich auf dem Rechner des Benutzers befindet.

            information_window("Bitte wählen Sie eine Datei aus.")
            text_file = file_finder()
            #Wenn eine Textdatei ausgewählt wird, wird das Program fortgesetzt. 
            if text_file:
                pass

            #Wenn keine Textdatei ausgewählt wird, wird das Hauptmenue wieder aufgerufen. 
            else:
                print("Es wurde keine Datei ausgewaehlt")
                input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
                run_program()
                
            # file_import wird hier ausgefuehrt und nimmt text_file als Argument an.
            text_analysis = options_func_dict(text_file)

            # emoticon_emoji_erkenner wird hier ausgefuehrt. Es gibt als Wert ein Dictionary zurueck
            res_dict = emoticon_emoji_erkenner(text_analysis)

            # Rueckgabe der Ergebnisse
            output_results(res_dict, fiit_has_run=True)

        # Da die anderen Optionen keine Argumente benoetigen,koennen sie hier ausgefuehrt werden.
        elif "twitter_import" in str(options_func_dict):

            tweet = twitter_import()
            # emoticon_emoji_erkenner wird hier ausgefuehrt.
            # Es gibt als Wert ein Dictionary zurueck
            res_dict = emoticon_emoji_erkenner(tweet)

            # Rueckgabe der Ergebnisse
            output_results(res_dict, twit_has_run=True)

        # Zeitliche Analyse der Textauswertung
        elif "time_analysis_menu" in str(options_func_dict):
            time_analysis_menu(running_time)
        else:
            options_func_dict()

################ Aufruf des Hauptprogramms ################

if __name__ == "__main__":
    # Wenn alle wichtige Dateien vorhanden sind, kann das Programm ausgefuehrt werden.
    if core_files_available:
        try:
            # Erstellung einer leeren Liste fuer die Laufdauerberechnung
            running_time = list()
            # Aufruf des Programms
            run_program()
        # Falls es einen Fehler bei der Ausfuehrung gibt, wird der Benutzer entsprechen informiert. 
        except Exception as error:
            print(error)
