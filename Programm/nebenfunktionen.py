'''
Hier sind zusaetzliche Funktionen gespeichert, die in das Hauptprogramm via Import importiert werden.
Die entsprechenden Beschreibung der Funktion sind bei der jeweiligen Funktionen.
'''

#########################
# Notwendige Pythonmodule
#########################

import re,os,shutil,tkinter
from datetime import datetime
from tkinter import filedialog, Tk, messagebox

#########################
# Importierung des Matplotlib-Moduls
#########################

#Es wird versucht, das Modul zu importierten. 
try:
    import matplotlib.pyplot as plt
    from matplotlib import figure
except ImportError:
    # Wenn der Benutzer matplotlib nicht schon vorher installiert hat, bekommt er eine Fehlermeldung.
    # Die Fehlermeldung wird hier ausgegeben.
    print(
        "\nDa das Modul 'matplotlib' nicht installiert ist bzw. nicht importiert werden kann,\nkann das Programm nicht wie vorgesehen ausgefuehrt werden. ")

    while True:
        # Hier hat der Benutzer die Moeglichkeit das Programm trotzdem auszufuehren.
        program_continue = input("\nWollen Sie das Programm trotzdem ausfuehren? (y/n) ").lower()

        # Zustimmung
        if program_continue == "y":
            # Das Programm wird ohne matplotlib ausgufuehrt. Eine Stabilitaet des Programms kann allerdings nicht gewaehrleistet werden.
            print("Die Weiternutzung des Programms ist eingeschraenkt, da 'matplotlib' nicht vorhanden ist.")
            break

        # Ablehnung
        elif program_continue == "n":
            # Das Programm wird bei einer Verneinung nicht ausgefuehrt.
            print("Das Programm wird sofort beendet.")
            raise SystemExit

        # Unbekannte bzw. falsche Antwort
        else:
            print(f"{program_continue} ist keine gueltige Antwort. Entweder 'y' oder 'n' eingeben.")

#########################
# Einlesen der Datenbanken
#########################

# Die Datenbank werden als Variablen gespeichert, damit sie nicht im Programm immer wieder abgetippt werden muessen.
program_emoticon_database = "Ressourcen/Emoticons_emoji_datenbank/emoticon_basisdatenbank.tsv"  # Programmdatenbank
user_emoticon_database = "Ressourcen/Emoticons_emoji_datenbank/emoticon_benutzerdatenbank.tsv"  # Benutzerdatenbank
emoji_database = "Ressourcen/Emoticons_emoji_datenbank/emoji_datenbank.tsv"  # Emojidatenbank

emoticon_dict, emoji_dict = dict(), dict()

# Programmdatenbank wird aufgemacht
with open(program_emoticon_database, mode="r", encoding="utf-8") as emoticon_file, \
        open(emoji_database, mode="r", encoding="utf-8") as emoji_file:

    '''
    Die Dateien werden eingelesen und die entsprechenden Dictionaries werden ergaenzt.
    Es wird immer das erste Element bzw. [0] an die entsprechende Liste angehangen,
    da das Emoticon bzw. Emoticon dort gespeichert ist. Danach werden die Dateien zugemacht. 
    '''
    for emoticon in emoticon_file: emoticon_dict[emoticon.split()[0]] = emoticon  # Emoticons
    for emoji in emoji_file: emoji_dict[emoji.split()[0]] = emoji  # Emojis

#########################
# Nebenfunktionen
#########################

'''
Ein Menuesystem, das im Programm aufgerufen werden kann.

Es nimmt drei Argumente:

output_menu {name der Funktion : funktion } ohne Klammern. 
menu_name - Name des Menues
menu_inforamtion - Information, die Unterhalb des Menuenamen angezeigt wird. 

'''
def menu(output_menu, menu_name, menu_information):
    invalid_option = f'Leider ist ein Fehler ist aufgetreten. Mit der Eingabetaste gelangen Sie wieder in das {menu_name}.'

    while True:
        print(f'\n\t\t~ {menu_name} ~\n')  # Name des Menues
        print(f'{menu_information}\n')  # Zugehoerige Information
        print("Hinweis: Gross- und Kleinschreibung muessen nicht bei der Eingabe beruecksichtigt werden\n")

        # Mit einer For-Schleife werden die Menupunkte aufgezaehlt.
        for num, elem in enumerate(output_menu, start=1):
            print(f'{num}: {elem}')

        # Der Benutzer wird aufgefordert sich eine Funktion ausgesucht.
        choice_str = input("\nEntweder die Nummer des Menuepunkts oder dessen Namen bitte eingeben:").strip()

        # Die entsprechende Funktion wird von menu_option entnommen und ausgefuehrt.
        menu_option = output_menu.get(choice_str.title())

        # Wenn die Eingabe sich mit einer Funktion in dem Dictionary uebereinstimmt, wird die Schleife gebrochen.
        if menu_option:
            break
        # Es wird geprueft, ob der Benutzer eine Ziffer eingegeben hat.
        else:
            try:
                # Die Funktion nummerisch aufrufen
                choice_num = int(choice_str)
            except:
                # Der Benutzer wird darauf hingewiesen, dass die numerische Eingabe ungueltig ist.
                input(invalid_option)
            else:
                if 0 < choice_num and choice_num <= len(output_menu):
                    # Die Werte (Funktionen) des Dictionarys werden als Liste gespeichert.
                    func_list = list(output_menu.values())
                    # Es wird aus dieser Liste die Funktion per Indizierung gezogen.
                    function_number = choice_num - 1
                    # Die Funktion
                    options_func_dict = func_list[function_number]
                    # Die Funktion wird weitergegben.
                    # Die Schleife wird gebrochen.
                    break
                else:
                    # Der Benutzer wird darauf hingewiesen, dass die Eingabe ungueltig ist.
                    input(invalid_option)

    # Die Option wird mit return wiedergeben, damit es von anderen Funktionen verarbeitet werden kann.
    try:  
        # Wenn die Funktion keine Argumente hat,
        # Wird nur die Funktion ausgefuehrt
        return options_func_dict()
        # Wenn die Funktionen Argumente hat,
        # werden die Ergebnisse ausgegeben.
    except Exception as error:
        return options_func_dict

'''
token_filter taggt die Tokens nach den angegebenen Regexausdruecken. 
Es wird im Hauptprogramm eingesetzt, um zu verhindern, dass Woerter faelscherweise als Emoticons
getaggt werden. Die Regextags in dieser Funktion sind somit eher intern und tauchen nicht im Programm auf. 
'''

def token_filter(token_list):

    # Die Ergebnisse der potenziellen Emoticons werden hier gespeichert.
    potenzielle_emoticons = list()

    # Sonderbuchstaben, die in fremden europaeischen Sprachen auftreten koennen z.B. im Spanischen, Italienischen.
    special_letters=r'ÀÂÄÇÈÉÊÎÔÖÙÛÜssÀÂÄÇÈÉÊÎÔÖÙÛÜÝĀÁÍŁÓŚĆĄÃĚŻàâäçèéêîôöùûüssàâäçèéêîôöùûüýāáíłóśćąãěż'

    # Gaenige Zeichensetzung
    punct_symbol="[\\/«»<>+&?='#%١٢٤!*()%;:\-+,\.]"

    # Regex besteht aus mehreren RA die durch | getrennt werden.
    # Das passende RA Dictionary bzw. Group wird mit einer For-Schleife ausgegeben.
    regex = re.compile(rf'''(?P<basic_word>^[/<[]*[A-Za-z{special_letters}]+[A-Za-z{special_letters}]$)|# Normale Woerter
    (?P<mixed_word>[\/[<>\-][\w+]|[\w{3}]{punct_symbol}$)|# Woerter mit Zeichensetzungen
    (?P<word_contraction>^[A-Za-z{special_letters}]+\b[',!.?]*[A-Za-z{special_letters}]*$)|#Abkuerzungen
    (?P<user>^(@|@/|)[A-Za-z{special_letters}]+(:|[0-9])(.+)$)|# Benutzernamen
    (?P<time>([0-9]+)(:[0-9])(:[0-9]+)*)|# Uhrzeit
    (?P<email>(\w+[.])*\w+@\w+[.]\w+)|# Emailaddressen 
    (?P<website>^(https://|http://)*(www)*[A-Za-z]+[.][A-Za-z]+(.+)$)|# Webseite
    (?P<hashtag>[#]\w{3,}|(\[)[#](.+)(]))|# Hashtags
    (?P<numbers>[%]*[\d+])|# Ziffern
    (?P<abbreviations>^[A-Z]+(.+)[0-9]*|[0-9]([amAM]|[pmPM]))|# Abkuerzungen
    (?P<common_commbinations>(->)+|(--)+|(,-)+$|(amp)|(:&))|# Kombination, die in den Texten haeufig vorkommen.
    (?P<punct_sym>^{punct_symbol}$|(=))+# Zeichensetzung ''', re.VERBOSE)  # Verbose erlaubt Kommentare

    # Mit einer For-Schleife werden die Tokens entsprechend getaggt.
    for token in token_list:
        # Wenn ein Match gefunden wird, wird das Token gezeigt.
        if regex.search(token):
            # Wenn ein Match Objekt vorhanden ist,  wird das dict davon erzeugt.
            regex_search_dict = regex.search(token).groupdict()
            # Anhand des Wertes wird der passende Schluessel bzw. Wortklasse ermittelt.
            '''
            Da es nur ein gueltiges Schluessel-Wert-Paar im Dictionary geben kann, sind die anderen == None .
            Z.B. {'cap': None, 'date': None, 'card': None,etc.'}
            Mit der If-Bedinung werden diese None-Objekte ignoriert. es wird als das Paar gewaehlt, dass eine Wortklasse hat.
            '''
            for (wert, schluessel) in regex_search_dict.items():
                # Das gueltige Paar wird in die Liste regex_ergebnisse angehangen.
                if schluessel != None:potenzielle_emoticons.append((token, wert))
        else:
            # Wenn dem Token kein passender Tag zugeordnet werden kann, bekommt das Token automatisch den Tag 'potenzielles_emoticon'
            # Diese Tags werden dann von den Emoticon und Emoji Erkenner weiter verarbeitet.
            potenzielle_emoticons.append((token, "potenzielles_emoticon"))

    # Rueckgabe der Ergebnisse
    return potenzielle_emoticons

'''
Die Funktion hat ein Argument 'text' und tokenisiert und paarst sie entsprechend. 
Personbezogene Daten z.b. Hashtags,Webseiten, etc, die oft in Tweets gefunden werden, werden entsprechend anonymisiert.  
'''

def tokenizer(text):

    # Hier werden die Tokens gespeichert.
    tokens = list()
    for row in text:

        # Satzzeichen, Emoticons und Emojis werden durch Leerzeichen ergaenzt, damit sie leichter tokenisiert werden koennen.
        # Es wird darauf geachtet, dass sie nicht von Emoticons oder potenziellen Emoticons entfernt werden.

        # Regeluaere Ausdruecke, die beim Tokenisieren eingesetzt werden:

        # Zeichensetzungen
        punctuation = re.findall(r"[a-zA-Z]{2,}[:]+|[,.!?*\"\']", row)

       # Klammern
        brackets = re.findall(r"\([a-zA-ZÄÖÜäöüß]{2,}\)*|\([a-zA-ZÄÖÜäöüß]{2,}|[a-zA-ZÄÖÜäöüß]{2,}\)", row)

       # Bestimmung der Uhrzeit, damit sie nicht falsch gepaarst werden.
        time_date = re.compile("[0-9]{2}:[0-9]{2}:*[0-9]{0,2}|^\d\d?\.\d\d?\.*(\d{2}|\d{4})*")

        # Entfernung der Hashtags, Benutzernamen, E-mailadresse und Webseiten mit naiven regulaeren Ausdruecken.
        row = re.sub("(\w+[.])*\w+@\w+[.]\w+", "emailadresse-entfernt", row)
        row = re.sub("(@\w+)|(@[/]+[\w]+)", "Benutzer-entfernt", row)  # Benutzername
        row = re.sub("#\w{3,}", "Hashtag-entfernt", row)  # Hashtag
        row = re.sub("(https://|www.)[/w\w+.]+", "Link-entfernt", row)  # Internetseiten

        # Emoticons von den Tokens trennen
        for emoticon in emoticon_dict.keys():
            # Ergaenzung der Emoticons durch Leerzeichen
            if emoticon in row.split():
                # Uhrzeiten und Daten ausschliessen, da sie falscherweise als Emoticons erkannt werden koennten.
                if time_date.findall(row):
                    row = row.replace(emoticon, " " + emoticon + "  ")

        # Emojis von den Tokens trennen
        for emoji in emoji_dict.keys():
            # Ergaenzung der Emoticons durch Leerzeichen
            if emoji in row:
                row = row.replace(emoji, " " + emoji + "  ")

        # Satzzeichen von den Tokens trennen
        for word in punctuation:
            # Doppelpunkte werden anders behandelt, damit sie nicht aus Versehen von Emoticons getrennt werden.
            if ":" in word and word in row and word[0].isnumeric() == False:
                # Aus Hello: wird Hello :
                colon = word.index(":")
                row = row.replace(word, word[:colon] + " " + word[colon:])
            else:
                # Bei den anderen Zeichen wird es durch Leerzeichen ergaenzt z.B. Hey. Hey .
                row = row.replace(word, f"  {word}  ")

        # Klammern von den Tokens trennen
        for word in brackets:
            # Wenn ein Klammer nur am Anfang und am Ende vorkommt.
            if "(" == word[0] and ")" == word[-1]:
                row = row.replace(word, word[0] + " " + word[1:-1] + " " + word[-1])
            elif "(" == word[0] and ")" != word[-1]:
                # Wenn ein Klammer nur am Anfang vorkommt.
                row = row.replace(word, " ( " + word[1:])
            else:
                # Wenn ein Klammer nur am Ende vorkommt.
                row = row.replace(word, word[:-1] + " ) ")

            # Die Zeile wird entsprechend gepaarst und tokenisiert.
        tokens.extend(row.split())

    # Wiedergabe der Tokens
    return tokens

'''
Es wird per Tkinter ein Dialogfenster aufgerufen, 
damit der Benutzer sich einen .txt-Datei auf seinem Rechner aussuchen kann.
Diese Datei wird dann von dem Programm entsprechend verarbeitet.  
'''
def file_finder():
    # Tk wird aufgerufen
    root = Tk()
    #Das TKFenster steht im Vordergrund, damit der Benutzer das Fenster nicht übersieht.
    root.attributes("-topmost", True)
    #Das Tkfenster wird zugemacht.
    root.withdraw()
    #Root-fenster wird zugemacht
    # Dialogfenster fuer die Dateien
    filename = filedialog.askopenfilename()
    # Der Pfadname der Datei wird zurueckgegeben. Diesen muss man entsprechend aufmachen.
    root.withdraw()
    return filename

# Hinweis fenster mit Tkinter
def information_window(message):
    #Ein Tkfenster wird aufgerufen
    root = tkinter.Tk()
    #Das Fenster steht im Vordergrund, damit der Benutzer das Fenster nicht übersieht
    root.attributes("-topmost", True)
    #Das Fenster wird wieder zugemacht 
    root.withdraw()
    #Information
    messagebox.showinfo("Information", message)


# Diese Funktion nimmt ein Dictionary als Argument an. Die Ergebnisse werden dann in Idle spaltenweise ausgegeben.
#wenn rel_has_run = True,  werden zusaetzliche Ergebnisse mitausgegeben werden.
''' Bei True: 
Anzahl saemtlicher Tags		3004
Anzahl falscher Tags		0
uebereinstimmung		100.0
Fehlerrate		0.0
Token		Goldtag		Programmtag
'''
def idle_results(res_dict,rel_has_run=False):
    if rel_has_run:
        i = 0  # Zaehler fuer die For-Schleife
        for key in res_dict:
            # Es werden die ersten 5 Zeile anders behandelt, da sie die Struktur und Ergebnisse
            # der Datei erklaeren. Die anderen Zeilen sind die Tokens und Tags.
            if i < 5:
                i += 1
                print(f"{key}\t\t{res_dict[key]}\n")
                # Nach der fuenften Zeile werden die Ergebnisse gleich a
            else:
                # If-Elif entscheidet die Menge an benoetigten Tabulatoren zwischen Schluessel und Wert
                if len(key) >= 8:
                    print(f"{key[1]}\t\t{res_dict[key]}\n")
                else:
                    print(f"{key[1]}\t\t\t{res_dict[key]}\n")
    else:
        # Je nach laenge des Wortes oder Emoticon/Emoji wird dieses sowie seine Klassifizierung in die Konsole ausgegeben.
        for line,key in enumerate(res_dict,start=1):
            # If-Elif bestimmen je nach Laenge des Schluessels die Menge an benoetigten Tabulatoren zwischen Schluessel und Wert.
            if len(key) >= 8:
                print(f"{line}\t{key[1]}\t{res_dict.get(key)}")
            elif len(key) >= 4:
                print(f"{line}\t{key[1]}\t\t{res_dict.get(key)}")
            else:
                 print(f"{line}\t{key[1]}\t\t\t{res_dict.get(key)}")

# Programminformationen werden mit dieser Funktion ausgegeben
def program_information():
    print("\nProgramminformation\n")
    # Die Information wird als ein Dictionary gespeichert.
    information_dict = { "Name:": "Emoji- und Emoticon-Erkenner",
                        "Version:": "1.0",
                        "Versionsdatum:": "10.09.2020",
                        "Programmierer:": "Christopher Chandler, Gianluca Cultraro"}
    
    # Ausgabe der Information ueber das Programm
    for entry in information_dict: print(entry,information_dict[entry])
    input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")

# Das Programm kann durch diese Funktion beendet werden.
def program_end():
    # Der Benutzer bekommt die Moeglichkeit, seine Antwort nochmal zu bestaetigen.
    while True:
        final_answer=input("⚠️ Wollen Sie das Programm wirklich beenden?(y/n) ⚠️").lower()
        if final_answer == "y":
            print ("Das Programm wird jetzt beendet.")
            # Beenden des Programms
            raise SystemExit
        # Ablehnung
        elif final_answer == "n":
            print("Das Programm wird nicht beendet. Sie werden zum Hauptmenue weitergeleitet.")
            input("Druecken Sie die Eingabetaste, um fortzufahren: ")
            break
        # Unbekannte bzw. falsche Antwort
        else:
            print(f"{final_answer} ist keine gueltige Antwort. Entweder 'y' oder 'n' eingeben.")


# Die Emoticons der Benutzerdatenbank kann durch diese Funktion leergemacht werden.
def delete_user_emoticons():
    # Pfadangabe der Datenbank
    user_emoticon_database = "Ressourcen/Emoticons_emoji_datenbank/emoticon_benutzerdatenbank.tsv"
    
    # Die While-Schleife bleibt solange bestehen, bis der Benutzer eine richtige Eingabe gemacht hat.
    while True:
       # Es wird geprueft, ob die Datenbank nicht existiert.
       if os.path.exists(user_emoticon_database) is not True:
            # Wenn dies der Fall ist, wird die folgende Information angezeigt.
            print( "Die Benutzerdatenbank ist momentan nicht vorhanden. Diese wird erst nach der ersten Textanalyse erstellt.")
            input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
            break
            
       # Der Benutzer bekommt die Moeglichkeit, seine Antwort nochmal zu bestaetigen.
       answer=input("⚠️ Sind Sie sich sicher, dass Sie Ihre Emoticondatenbank wirklich loeschen wollen ? Dies kann nicht rueckgaengig gemacht werden.⚠ (y/n)").lower()
       if os.path.exists(user_emoticon_database) and answer == "y":
            os.remove(user_emoticon_database)# Entfernung der Benutzerdatenbank
            print("Ihre Datenbank wurde geloescht.")
            input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
            break
       # Die Datenbank wird bei einer Verneinung nicht geloescht.
       elif answer == "n":
            print("Ihre Datenbank wurde nicht geloescht.")
            input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
            break

# Die Ergebnisse der Auswertungen kann durch diese Funktion geloescht werden.
def delete_result_folder():
    # Feststellen des Ortes des Ergebnisordners
    dirname = os.path.dirname(__file__)
    output_folder = os.path.join(dirname, "Ergebnisse")
    
    # Die While-Schleife bleibt solange bestehen, bis der Benutzer eine richtige Eingabe gemacht hat. 
    while True:
        # Es wird geprueft, ob die Datenbank nicht existiert. 
        if os.path.exists(output_folder) is not True:
            # Falls ja wird der Nutzer hierdrauf hingewiesen und die Schleife abgebrochen
            print("Dieser Ordner ist momentan nicht vorhanden. Ihr Ergebnisordner wird erst nach der ersten Ergebnisausgabe erstellt.")
            input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
            break
            
        # Der Benutzer bekommt die Moeglichkeit, seine Antwort nochmal zu bestaetigen.     
        answer = input("⚠️ Sind Sie sich sicher, dass Sie Ihren Ergebnisordner wirklich loeschen wollen ? Dies kann nicht rueckgaengig gemacht werden.⚠ (y/n)").lower()
         
        # Sollte der Ordner existieren und der Nutzer bejaht haben
        if os.path.exists(output_folder) and answer == "y":
            # wird der Ergebnisordner geloescht
            shutil.rmtree(output_folder, ignore_errors=True)
            print("Ihr Ergebnisordner wurde geloescht.")
            input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
            break
        # Die Datenbank wird bei einer Verneinung nicht geloescht.       
        elif answer == "n":
            print("Ihr Ergebnisordner wurde nicht geloescht.")
            input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
            break
         
# Output Menu mit internen Funktionen
# Alle Ausgaben finden in der Konsole statt
# Die Sekundenanzahlen werden mit 4 Nachkommastellen angegeben
def time_analysis_menu(running_time):
    # Ausgabe des letzten Vorgangs
    def current_running_time():
        # Die letzten drei Zeiten werden summiert und ausgegeben, da ein Vorgang aus drei Berechnungen besteht.
        print(f"Die Dauer des letzten Vorgangs betraegt: {sum(running_time[-3:]):0.4f}")
        input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptenue zu gelangen.")
        
    # Ausgabe aller gespeicherter Zeiten
    def all_running_time():
        print(f"Die Dauer aller Vorgaenge betraegt: {sum(running_time):0.4f}\n")
        input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptenue zu gelangen.")

    # Loeschen der schon gespeicherten Zeiten
    def delete_times():
        while True:
            # Der Benutzer wird nach einer Einverstaendis gefragt
            choice = input("⚠ Sind Sie sicher, dass Sie die bisherigen Zeiten loeschen wollen?  Dies kann nicht rueckgaengig gemacht werden.⚠ (y/n)").lower()
            # Sollte die Liste leer sein, so wird der Benutzer darauf hingewiesen und die Schleife abgebrochen.
            if not running_time:
                print("Es sind noch keine Zeiten zum Loeschen vorhanden.")
                input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
                break
            # Sollte der Benutzer mit "Y" antworten, so wird die Liste geleert und die Schleife anschliessend abgebrochen
            elif choice == "y":
                running_time.clear()
                break
            # Sollte der Benutzer mit "N" antworten, so wird nur die Schleife abgebrochen
            elif choice == "n":
                print("Ihre Zeiten wurden nicht geloescht.")
                input("\nDruecken Sie die Eingabetaste, um wieder in das Hauptmenue zu gelangen.")
                break

    # Funktionsmenue
    time_menu = {"Die Dauer des letzten Vorgangs": current_running_time,
                "Die Dauer aller Vorgaenge": all_running_time,
                "Alle Zeiten loeschen": delete_times}

    # Menu name
    menu_name = f"\nZeit Berechnungen\n"

    # Hinweise innerhalbs des Menues
    menu_information = "Wie soll die berechnete Zeit ausgegeben werden?"

    # Das Menue wird aufgerufen.
    menu(time_menu, menu_name, menu_information)

# Auswertung der Ergebnisse
def output_results(res_dict, twit_has_run = False, fiit_has_run = False, rel_has_run = False):  

    # Ausgabe der Ergebnisse in der Konsole
    def display_results():
        print("Analyseergebnisse:\n")
        # Eine separate Funktion wird aufgerufen, um die Ergebnisse ordentlich in der Konsole wiederzugeben.
        idle_results(res_dict,rel_has_run)

    # Ausgabe der Ergebnisse als Datei
    def file_results(res_dict):
        # Je nachdem, welcher der drei Parameter der Funktion output_results True ist, wird der Name der Datei bestimmt
        if twit_has_run:    # Fuer Twitterdateien
            save_name = "Twitter"
        elif fiit_has_run:    # Fuer Textdateien_training
            save_name = "Text"
        elif rel_has_run:     # Fuer Abspeicherung der Verlaesslichkeitsanalysen_test
            save_name = "Verlässlichkeits"
        # Erstellen eines Zeitstempels
        fulldate = datetime.now()
        # Der Timestamp wird im Format Stunde-Minute_Tag_Monat_Jahr
        timestamp = fulldate.strftime("%H-%M_%d_%B_%Y")
        # Der Dateiname wird zusammengefuegt
        filename = f"{save_name}_Ergebnisse_{timestamp}.txt"
        # Zielposition fuer den Ergebnissorder wird festgestellt
        dirname = os.path.dirname(__file__)
        # Zielposition und Ordnername werden zusammengefuegt
        folderpath = os.path.join(dirname, "Ergebnisse")
        # Der Ergebnisordner wird erstellt
        os.makedirs(folderpath, exist_ok=True)
        # Speicherort fuer die Datei wird festgesetzt
        savefile = os.path.join(dirname, "Ergebnisse", filename)

        # Neue Ergebnissdatei wird geschrieben
        file = open(savefile, mode="w", encoding="utf-8")

        # Je nach Laenge des Wortes oder Emoticon/Emoji wird dieses sowie seine Klassifizierung in das Ergebnislexikon geschrieben
        if rel_has_run:
            i=0 # Zaehler fuer die For-Schleife
            for key in res_dict:
                # Es werden die ersten 5 Zeile anders behandelt, da sie die Struktur und Ergebnisse
                # der Datei erklaeren. Die anderen Zeilen sind die Tokens und Tags.
                if i < 5:
                    i+=1
                    file.write(f"{key}\t\t{res_dict[key]}\n")
                    #Nach der fuenften Zeile werden die Ergebnisse gleich a
                else:
                    # If-Elif entscheidet die Menge an benoetigten Tabulatoren zwischen Schluessel und Wert
                    if len(key) >= 8:
                        file.write(f"{key[1]}\t\t{res_dict[key]}\n")
                    else:
                        file.write(f"{key[1]}\t\t\t{res_dict[key]}\n")
            file.close()
        # Bei Tweets oder Text Dateien werde die Ergebnisse anders ausgegeben.
        elif twit_has_run==True or fiit_has_run==True:
            for key in res_dict:
                # If-Elif entscheidet die Menge an benoetigten Tabulatoren zwischen Schluessel und Wert
                if len(key) >= 8:
                    # key[0] damit die Nummerierung der aus dem Dictionary entfernt wird.
                    file.write(f"{key[0]}\t{res_dict.get(key)}\n")
                else:
                    file.write(f"{key[1]}\t\t\t{res_dict.get(key)}\n")
            file.close()

    # Funktion zum Aufrufen beider Optionen
    def both_results():
        display_results()
        file_results(res_dict)
    
    # Funktionsmenue
    output_menu = {"Konsole": display_results,
                   "Datei": file_results(res_dict),
                   "Konsole + Datei": both_results}

    # Menu Name
    menu_name = '\nAusgabemenue\n'
    # Menu Info
    menu_information = 'Wie sollen die Ergebnisse ausgegeben werden?\n'
    # Aufruf des Menu
    menu(output_menu, menu_name, menu_information)

'''
Mit dieser Funktion wird eine graphische Darstellung der Ergebnisse erzeugt. 
Diese erscheint anschliessend im Ergebnisordner. 
'''
def bar_chart(values_list):
    # Die Werte auf der X-Achse
    x_achse = [f'Emoticons\n{values_list[0]}', f'Emojis\n{values_list[1]}',
         f'Neubildung\n{values_list[2]}', f'Rest\n{values_list[3]}']
    # Die Farben der Balken
    colors = ["gold", "royalblue", "purple", "teal"]
    # Die Werte in der values_liste
    values = values_list

    # Erstellung der X-Werte
    x_pos = [i for i, _ in enumerate(x_achse)]

    # Erstellung der Balken
    plt.bar(x_pos, values, color=colors)

    # Beschriftung des Graphen
    plt.xlabel("Tokenkategorie")
    plt.ylabel("Anzahl der Tokens")
    plt.title(f"Auswertung")

    # Der Timestamp wird im Format Stunde-Minute_Tag_Monat_Jahr
    fulldate = datetime.now()
    timestamp = fulldate.strftime("%H-%M_%d_%B_%Y")

    # Der Dateiname wird zusammengefuegt, damit die Verlaesslichkeitsdatei und die Darstellung den gleichen Namen bis auf die Endung tragen.
    filename = f"Ergebnisse/Verlässlichkeits_Ergebnisse_{timestamp}.png"
    plt.xticks(x_pos, x_achse)

    # Ergaenzung des Graphen, damit die Beschriftung auf der X-Achse komplett angezeigt wird.
    plt.gcf().subplots_adjust(bottom=0.15)

    # Erstellung der Datei in dem Ordner.
    plt.savefig(filename, dpi=500)
