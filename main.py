"""
main.py

    Startet das Programm

        fehlende Module:
            (pyinstaller), tomlkit, guizero, openai, edge-tts

        mit pyinstaller: pyinstaller --onefile --windowed main.py

"""

# -----------------------------------------------------------------------------
import guizero as gz

from script_dir import helfer


# -----------------------------------------------------------------------------
def main() -> bool:
    """
    Startet die GUI
    :return: True, wenn alles OK
    """

    print()
    print(60 * "x")
    print("Starte GUI")

    # Funktion, die aufgerufen wird, wenn ein Button gedrückt wird
    def button_clicked(button_text):
        print(f"Button '{button_text}' wurde geklickt!")

    # Hauptfenster erstellen
    app = helfer.APP

    # kann nicht vergrössert werden
    app.tk.resizable(False, False)

    # Fonts
    app.font = "Helvetica"
    app.text_size = 16

    # Button: neuer Text erstellen
    gz.PushButton(
        master=app,
        text="Texte erstellen",
        width=100,
        command=helfer.klicke_button_text_erstellen,
    )

    # # Button: bestehender Text normalisieren
    # gz.PushButton(master=app, text='Texte normalisieren', width=100,
    #              command=helfer.klicke_button_text_normalisieren)

    # Button: bestehender Text bearbeiten
    gz.PushButton(
        master=app,
        text="Texte bearbeiten",
        width=100,
        command=helfer.klicke_button_text_bearbeiten,
    )

    # Button: Text vereinfachen
    gz.PushButton(
        master=app,
        text="Texte vereinfachen",
        width=100,
        command=helfer.klicke_button_text_vereinfachen,
    )

    # Button: Fragen zu Text suchen
    gz.PushButton(
        master=app,
        text="Fragen suchen",
        width=100,
        command=helfer.klicke_button_fragen_suchen,
    )

    # Button: Text zu Audio
    gz.PushButton(
        master=app,
        text="Text zu Audio",
        width=100,
        command=helfer.klicke_button_text_zu_audio,
    )

    # Button: Erstelle alle html-Inhalte
    gz.PushButton(
        master=app,
        text="Texte zu html",
        width=100,
        command=helfer.klicke_button_texte_zu_html,
    )

    # Button: Speichere die Texte im Internet
    gz.PushButton(
        master=app,
        text="Texte ins Internet",
        width=100,
        command=helfer.klicke_button_texte_ins_internet,
    )

    # Button: Text zu Podcast
    gz.PushButton(
        master=app,
        text="Texte zu Podcast",
        width=100,
        command=helfer.klicke_button_text_zu_podcast,
    )

    # Button: Lesbarkeit der Texte
    gz.PushButton(
        master=app,
        text="Lesbarkeit der Texte",
        width=100,
        command=helfer.klicke_button_lesbarkeit_texte,
    )

    # Button: Budget bei OpenAI
    gz.PushButton(
        master=app,
        text="Budget bei OpenAI",
        width=100,
        command=helfer.klicke_button_budget_bei_openai,
    )

    # Buttons erstellen und hinzufügen
    # button1 = gz.PushButton(app, text="Button 1", command=lambda: button_clicked("Button 1"))

    # Startet das Hauptfenster
    app.display()

    return True


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    
    main()

#     podcast_text = """
# **Tom:** Hallo und herzlich willkommen zu unserem Podcast! Ich bin Tom und heute habe ich eine ganz besondere Expertin bei mir, Lisa. 

# **Lisa:** Hallo Tom, schön hier zu sein! Ich freue mich darauf, mit dir über die spannende Geschichte der Städte im Mittelalter zu reden.

# **Tom:** Ja, das klingt super! Aber bevor wir starten, kannst du uns kurz erklären, was eigentlich das Mittelalter ist?

# **Lisa:** Natürlich! Das Mittelalter ist eine Zeit in der Geschichte, die von etwa 500 bis 1500 nach Christus dauerte. Das ist also schon eine ganz schöne Weile her!

# # **Tom:** Wow, das ist eine lange Zeit! Und was passiert denn da genau, Lisa?

# # **Lisa:** Ich danke dir, Tom! Es hat viel Freude gemacht, über dieses Thema zu sprechen. Bis zum nächsten Mal!

# # **Tom:** Bis zum nächsten Mal! Und liebe Zuhörer, bleibt neugierig und denkt daran, dass Geschichte echt spannend ist! Tschüss!

#     """

#     helfer.mache_podcast_zu_audio(datei_name='mittelalter-stadt.toml', podcast_text=podcast_text)
