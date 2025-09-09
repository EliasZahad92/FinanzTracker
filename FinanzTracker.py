eintraege = []

df = pd.read_csv("LADE HIER DEINE DATEI HOCH!!!!!!!!!!!", encoding="ISO-8859-1", sep=";")
df["Betrag"] = (
    df["Betrag"]
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)
for index, zeile in df.iterrows():
    beschreibung = zeile["Verwendungszweck"]
    betrag = zeile["Betrag"]
    eintraege.append((beschreibung, betrag))

def generate_pdf(eintraege, pfad="output/Finanzbericht.pdf"):
    os.makedirs("output", exist_ok=True)
    doc = SimpleDocTemplate(pfad, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    titel = Paragraph("Finanzbericht", styles["Title"])
    elements.append(titel)
    elements.append(Spacer(1, 12))

    if not eintraege:
        elements.append(Paragraph("Keine Einträge vorhanden.", styles["Normal"]))
    else:
        daten = [("Beschreibung", "Betrag (€)")] + [(b, f"{betrag:.2f}") for b, betrag in eintraege]
        tabelle = Table(daten, colWidths=[350, 100])
        tabelle.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(tabelle)

    doc.build(elements)
    print(f"PDF wurde erstellt: {pfad}")

print("FinanzTracker: Herzlich Willkommen!")

while True:
    try:
        frage = int(input("Was möchtest du vornehmen? (1: Eintrag, 2: Anzeigen, 3: Beenden, 4: PDF): "))
        if frage == 1:
            try:
                beschreibung = input("Wofür wurde der Betrag genutzt?: ").strip()
                betrag = float(input("Betrag in Euro: "))
                eintraege.append((beschreibung, betrag))
                print("Betrag wurde eingespeichert!")
            except ValueError:
                print("Bitte gebe einen gültigen Betrag ein: ")
        elif frage == 2:
            if not eintraege:
                print("Keine Einträge vorhanden")
            else:
                print("\nAlle Einträge:")
                for i, (beschreibung, betrag) in enumerate(eintraege, start=1):
                    print(f"{i}. {beschreibung} - {betrag:.2f} €.")
        elif frage == 3:
            print("Programm verlassen")
            break
        elif frage == 4:
            generate_pdf(eintraege)
        else:
            print("Bitte gebe eine gültige Zahl an! (1-4): ")
    except ValueError:
        print("Bitte eine gültige Zahl eingeben")
