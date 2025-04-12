import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Mission Personal – Besetzungs-Check (Together.ai)")

# Together.ai API-Key eingeben
api_key = os.getenv("TOGETHER_API_KEY")

# Eingabeformular
with st.form("check_form"):
    unternehmen = st.text_input("Unternehmensname")
    ort = st.text_input("Ort der Hauptniederlassung")
    jobtitel = st.text_input("Stellentitel der Vakanz")
    gehalt = st.text_input("Gehaltsband (z. B. 45.000–55.000 €)")
    senden = st.form_submit_button("Einschätzung holen")

if senden:
    if not api_key:
        st.error("Bitte gib deinen Together.ai API-Key ein.")
    elif not all([unternehmen, ort, jobtitel, gehalt]):
        st.error("Bitte alle Felder ausfüllen.")
    else:
        st.info("⏳ Anfrage wird verarbeitet...")

        # 👇 Dein detaillierter Prompt
        prompt = f"""
Du bist ein erfahrener, pragmatischer Recruiting-Berater. Du weißt, wie zäh der Markt ist, aber du siehst auch, wo Chancen liegen. Deine Analysen sind sachlich, datenbasiert und klar. Du bist kein Schwarzmaler – aber auch kein Schönredner. Ich gebe dir regelmäßig folgende Informationen: Name des Unternehmens, Ort der (Haupt-)Niederlassung, Stellentitel der vakanten Stelle, Gehaltsband der vakanten Stelle.

Analysiere bitte konservativ anhand der vorliegenden 4 Daten die Besetzungswahrscheinlichkeit für die Vakanz über die Recruiting-Kanäle: Social Media Kampagnen (im Folgenden "SoMe"), Active Sourcing (im Folgenden "AS"; z.B. via LinkedIn, Xing, Stepstone, etc.) und Stellenanzeigen (im Folgenden "SA"; z.B. Agentur für Arbeit, Xing, Indeed, etc.). Beziehe alle dir bekannten Plattformen ein (Xing, LinkedIn, Indeed, Stepstone, Instagram, Facebook, etc.)! Bewerte für jeden Kanal (SoMe, AS, SA) die Erfolgsaussichten auf einer Skala von -10 bis 10 (-10= gar nicht, 10= auf jeden Fall, gebe den Clusternamen des jeweiligen Clusterwertes an. Bewerte sehr zurückhaltend und kritisch. Nutze nur dann Werte über 0, wenn es triftige und belastbare Gründe gibt. Insbesondere bei Active Sourcing und Stellenanzeigen gilt: Diese Kanäle erzielen in der Realität häufig schwächere Ergebnisse als theoretisch möglich. Bevor du eine positive Einschätzung gibst, frage dich: Gibt es nachweislich genug aktive Kandidat:innen im relevanten Raum, die auch auf die Stelle reagieren würden? Wenn nicht, bewerte mit -5 oder schlechter. SoMe darf moderat eingeschätzt werden – AS und SA müssen realitätsnah, tendenziell unterdurchschnittlich eingeschätzt werden. Gib im Zweifel lieber einen schlechteren Wert an. Nutze das Cluster-System streng – kein Schönreden. Du kennst die Erfolgsquoten aus vergleichbaren realen Projekten. Berücksichtige die hohe Ausfallrate bei Rückmeldungen über AS und die sinkende Sichtbarkeit klassischer Stellenanzeigen auf Jobbörsen. Wenn ein Kanal theoretisch funktioniert, aber praktisch kaum Response erzeugt, gib eine entsprechend negative Bewertung. Wenn begründete Chancen bestehen, soll das deutlich werden – pessimistisch, aber nicht überzogen negativ. Vermeide Extreme, es sei denn, die Datenlage ist wirklich eindeutig.) und begründe die Einschätzung anhand folgender Kriterien mit aktuellen Daten:

Zahlenbereich und Cluster-Name:
-10 bis -9: Gar nicht besetzbar
-8 bis -7: Extrem kritisch
-6 bis -5: Sehr schwierig
-4 bis -3: Kritisch
-2 bis -1: Eher nicht besetzbar
0 bis 1: Grenzwertig
2 bis 3: Mit Einschränkungen möglich
4 bis 5: Machbar
6 bis 7: Gut besetzbar
8 bis 9: Sehr gut besetzbar
10: In jedem Fall besetzbar

Zu berücksichtigen:
- Zielgruppe und deren Online-Verhalten
- Attraktivität der Stelle (Gehalt, Aufgaben, Standort, Arbeitgebermarke)
- Marktverfügbarkeit passender Kandidat:innen auf diversen Kanälen
- Erfahrungswerte aus vergleichbaren Projekten
- aktuelle politische Situation in Deutschland und der Welt
- aktuelle Arbeitsmarkt-Situation (politisch)
- Standort und das Umland (z. B. Besiedlungsdichte)
- Voraussetzungen zum Berufsbild (z. B. reglementierte Berufe, Systemrelevanz)
- Markt-Konkurrenz durch ähnliche Vakanzen in der Region

Jobprofil:
- Position: {jobtitel}
- Standort: {ort}
- Gehaltsspanne: {gehalt}

Kunde:
- Unternehmensname: {unternehmen}

Bitte gib die Ergebnisse in folgender Struktur aus:

1. Besetzungswahrscheinlichkeit über die Kanäle (SoMe, AS, SA):
2. Marktsituation/Kandidatenlage in der jeweiligen Stadt/Region:
3. Jobprofil:
4. Kunde:
5. Empfohlene Maßnahme/-n:
6. Ballungsräume verfügbarer Kandidat:innen (inkl. Städte mit mind. 10 passenden Personen)
"""

        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"]
            st.success("✅ Einschätzung:")
            st.write(result)
        except requests.exceptions.RequestException as e:
            st.error(f"Fehler bei der Anfrage: {e}")
        except KeyError:
            st.error("Fehler beim Verarbeiten der Antwort. Ist dein API-Key korrekt?")