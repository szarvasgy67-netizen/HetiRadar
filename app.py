import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="HetiRadar - Heti Hírek Összefoglaló",
    page_icon="🌍",
    layout="wide"
)

# --- KEZDŐ HÍRADATBÁZIS (Minta heti összefoglaló) ---
INITIAL_NEWS = [
    # MAGYARORSZÁG
    {
        "het": "2026. 48. hét",
        "regio": "Magyarország",
        "kategoria": "Gazdaság",
        "fontossag": "Kritikus",
        "cim": "MNB kamatdöntés és friss inflációs előrejelzés",
        "osszefoglalo": "A jegybank a várakozásoknak megfelelően tartotta az alapkamatot, miközben hangsúlyozta a forint árfolyamstabilitásának fontosságát. A friss elemzések szerint az év végi infláció a célsáv felső szélén alakulhat."
    },
    {
        "het": "2026. 48. hét",
        "regio": "Magyarország",
        "kategoria": "Politika",
        "fontossag": "Fontos",
        "cim": "Jövő évi költségvetési módosítások az Országgyűlés előtt",
        "osszefoglalo": "A kormány benyújtotta a jövő évi adó- és költségvetési csomagot, amely kiemelt támogatást irányoz elő a kis- és középvállalkozások digitalizációjára és az energetikai korszerűsítésekre."
    },
    {
        "het": "2026. 48. hét",
        "regio": "Magyarország",
        "kategoria": "Kultúra",
        "fontossag": "Átlagos",
        "cim": "Rekordlátogatottság a budapesti őszi múzeumi fesztiválon",
        "osszefoglalo": "Több mint százezer látogatót vonzottak a fővárosi és vidéki kiállítóterek tematikus tárlatvezetései, különösen a kortárs magyar fotóművészeti tárlatok voltak népszerűek."
    },
    # EURÓPA
    {
        "het": "2026. 48. hét",
        "regio": "Európa",
        "kategoria": "Gazdaság",
        "fontossag": "Kritikus",
        "cim": "EU-s ipari versenyképességi csomag és energiapiaci reform",
        "osszefoglalo": "Az Európai Bizottság új intézkedéscsomagot terjesztett elő az ipari energiaárak csökkentésére és a zöldtechnológiai beruházások gyorsított engedélyezésére."
    },
    {
        "het": "2026. 48. hét",
        "regio": "Európa",
        "kategoria": "Politika",
        "fontossag": "Fontos",
        "cim": "Uniós csúcstalálkozó a közös védelmi beszerzésekről",
        "osszefoglalo": "A tagállamok vezetői megállapodtak a határokon átnyúló védelmi ipari projektek közös finanszírozási keretének bővítéséről."
    },
    {
        "het": "2026. 48. hét",
        "regio": "Európa",
        "kategoria": "Kultúra",
        "fontossag": "Átlagos",
        "cim": "Kihirdették a jövő évi Európa Kulturális Fővárosa programsorozatát",
        "osszefoglalo": "Számos ingyenes szabadtéri koncerttel, digitális művészeti installációval és európai színházi találkozóval készülnek a házigazda városok."
    },
    # USA
    {
        "het": "2026. 48. hét",
        "regio": "USA",
        "kategoria": "Gazdaság",
        "fontossag": "Kritikus",
        "cim": "Fed jegyzőkönyv: óvatosabb kamatcsökkentési pálya körvonalazódik",
        "osszefoglalo": "Az amerikai jegybank döntéshozói az erős munkaerőpiaci adatok miatt lassabb ütemű monetáris lazítást vetítettek előre, ami erősítette a dollárt."
    },
    {
        "het": "2026. 48. hét",
        "regio": "USA",
        "kategoria": "Politika",
        "fontossag": "Fontos",
        "cim": "Kétpárti egyeztetés a mesterséges intelligencia szabályozásáról",
        "osszefoglalo": "A szenátusi bizottság új átláthatósági és szerzői jogi irányelveket javasolt a nagy nyelvi modelleket fejlesztő technológiai cégek számára."
    },
    {
        "het": "2026. 48. hét",
        "regio": "USA",
        "kategoria": "Kultúra",
        "fontossag": "Átlagos",
        "cim": "Független filmek taroltak az őszi amerikai fesztiválszezonban",
        "osszefoglalo": "A kritikusok szerint idén a kisebb költségvetésű, társadalmi drámák dominálják a díjszezon előzetes esélylatolgatásait."
    },
    # ÁZSIA
    {
        "het": "2026. 48. hét",
        "regio": "Ázsia",
        "kategoria": "Gazdaság",
        "fontossag": "Kritikus",
        "cim": "Félvezető-ellátási láncok bővítése Kelet-Ázsiában",
        "osszefoglalo": "Dél-Korea és Tajvan vezető chipgyártói újabb milliárdos beruházásokat jelentettek be a következő generációs AI-processzorok gyártókapacitásának növelésére."
    },
    {
        "het": "2026. 48. hét",
        "regio": "Ázsia",
        "kategoria": "Politika",
        "fontossag": "Fontos",
        "cim": "ASEAN kereskedelmi fórum a digitális vámeljárásokról",
        "osszefoglalo": "A délkelet-ázsiai országok megállapodtak az elektronikus kereskedelmi dokumentáció egységesítéséről a régiós áruforgalom gyorsítása érdekében."
    },
    {
        "het": "2026. 48. hét",
        "regio": "Ázsia",
        "kategoria": "Kultúra",
        "fontossag": "Átlagos",
        "cim": "Tokiói dizájnhét: fenntartható építészet és hagyományos kézművesség",
        "osszefoglalo": "A kiállítás fókuszában a hagyományos japán faépítészeti technikák és a modern, újrahasznosított anyagok ötvözése állt."
    }
]

# Munkamenet-állapot inicializálása, hogy új híreket is lehessen hozzáadni
if "news_list" not in st.session_state:
    st.session_state.news_list = INITIAL_NEWS.copy()

# Segédfüggvény a fontossági jelvényhez
def get_priority_badge(level):
    if level == "Kritikus":
        return "🔴 KRITIKUS"
    elif level == "Fontos":
        return "🟠 FONTOS"
    else:
        return "🟢 ÁTLAGOS"

def render_news_cards(df_filtered):
    if df_filtered.empty:
        st.info("Nincs a kiválasztott szűrőknek megfelelő hír ebben a kategóriában.")
        return
    
    # Rendezés fontosság szerint: Kritikus -> Fontos -> Átlagos
    priority_order = {"Kritikus": 1, "Fontos": 2, "Átlagos": 3}
    df_filtered = df_filtered.copy()
    df_filtered["prio_rank"] = df_filtered["fontossag"].map(priority_order)
    df_filtered = df_filtered.sort_values(by=["prio_rank", "kategoria"])

    for _, row in df_filtered.iterrows():
        badge = get_priority_badge(row["fontossag"])
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{badge}**  |  📂 *{row['kategoria']}*  |  📅 `{row['het']}`")
                st.markdown(f"#### {row['cim']}")
                st.write(row["osszefoglalo"])
            with c2:
                st.markdown(f"**Régió:**\n{row['regio']}")
# --- FELÜLET FELÉPÍTÉSE ---
st.title("🌍 HetiRadar – Heti Világ- és Hazai Hírek")
st.markdown("Tömör, lényegre törő heti összefoglaló fontossági és tematikus bontásban.")

df_all = pd.DataFrame(st.session_state.news_list)

# --- OLDALSÁV: GLOBÁLIS SZŰRŐK ---
with st.sidebar:
    st.header("🔍 Szűrők")
    hetek = ["Összes hét"] + sorted(df_all["het"].unique().tolist(), reverse=True)
    valasztott_het = st.selectbox("📅 Hét kiválasztása:", hetek)
    
    valasztott_fontossag = st.multiselect(
        "🚨 Fontossági szint:",
        options=["Kritikus", "Fontos", "Átlagos"],
        default=["Kritikus", "Fontos", "Átlagos"]
    )
    
    valasztott_kategoria = st.multiselect(
        "📂 Témakör:",
        options=["Politika", "Gazdaság", "Kultúra"],
        default=["Politika", "Gazdaság", "Kultúra"]
    )

# Szűrés alkalmazása
df_filtered = df_all.copy()
if valasztott_het != "Összes hét":
    df_filtered = df_filtered[df_filtered["het"] == valasztott_het]
if valasztott_fontossag:
    df_filtered = df_filtered[df_filtered["fontossag"].isin(valasztott_fontossag)]
if valasztott_kategoria:
    df_filtered = df_filtered[df_filtered["kategoria"].isin(valasztott_kategoria)]

# --- ÖSSZESÍTŐ METRIKÁK ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Összes megjelenített hír", len(df_filtered))
m2.metric("🔴 Kritikus", len(df_filtered[df_filtered["fontossag"] == "Kritikus"]))
m3.metric("🟠 Fontos", len(df_filtered[df_filtered["fontossag"] == "Fontos"]))
m4.metric("🟢 Átlagos", len(df_filtered[df_filtered["fontossag"] == "Átlagos"]))

st.divider()

# --- RÉGIÓS FÜLEK + ÚJ HÍR RÖGZÍTÉSE ---
tab_hu, tab_eu, tab_us, tab_asia, tab_all, tab_add = st.tabs([
    "🇭🇺 Magyarország",
    "🇪🇺 Európa",
    "🇺🇸 USA",
    "🌏 Ázsia",
    "🌐 Összes régió",
    "➕ Új hír hozzáadása"
])

with tab_hu:
    st.subheader("🇭🇺 Magyarországi heti összefoglaló")
    render_news_cards(df_filtered[df_filtered["regio"] == "Magyarország"])

with tab_eu:
    st.subheader("🇪🇺 Európai heti összefoglaló")
    render_news_cards(df_filtered[df_filtered["regio"] == "Európa"])

with tab_us:
    st.subheader("🇺🇸 Egyesült Államok (USA) heti összefoglaló")
    render_news_cards(df_filtered[df_filtered["regio"] == "USA"])

with tab_asia:
    st.subheader("🌏 Ázsiai heti összefoglaló")
    render_news_cards(df_filtered[df_filtered["regio"] == "Ázsia"])

with tab_all:
    st.subheader("🌐 Összes régió hírei egyben")
    render_news_cards(df_filtered)

with tab_add:
    st.subheader("➕ Új heti hír rögzítése")
    st.caption("Itt gyorsan felvihetsz új híreket az aktuális munkamenetbe, majd CSV-ként letöltheted a frissített listát.")
    
    with st.form("uj_hir_form", clear_on_submit=True):
        c_f1, c_f2, c_f3 = st.columns(3)
        with c_f1:
            uj_regio = st.selectbox("Régió:", ["Magyarország", "Európa", "USA", "Ázsia"])
        with c_f2:
            uj_kat = st.selectbox("Kategória:", ["Politika", "Gazdaság", "Kultúra"])
        with c_f3:
            uj_prio = st.selectbox("Fontosság:", ["Kritikus", "Fontos", "Átlagos"])
            
        uj_het = st.text_input("Hét megjelölése:", value="2026. 48. hét")
        uj_cim = st.text_input("Hír rövid címe:")
        uj_szoveg = st.text_area("Nagyon rövid összefoglaló (2-3 mondat):", height=100)
        
        submitted = st.form_submit_button("Hír hozzáadása a listához")
        if submitted:
            if uj_cim.strip() and uj_szoveg.strip():
                st.session_state.news_list.insert(0, {
                    "het": uj_het.strip(),
                    "regio": uj_regio,
                    "kategoria": uj_kat,
                    "fontossag": uj_prio,
                    "cim": uj_cim.strip(),
                    "osszefoglalo": uj_szoveg.strip()
                })
                st.success("Hír sikeresen hozzáadva! Nézd meg a megfelelő régió fülén.")
                st.rerun()
            else:
                st.error("Kérlek, add meg a hír címét és rövid összefoglalóját is!")
                
    # Letöltési lehetőség biztonsági mentéshez
    csv_data = pd.DataFrame(st.session_state.news_list).to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 Teljes hírlista letöltése CSV-ben",
        data=csv_data,
        file_name="hetiradar_hirek.csv",
        mime="text/csv"
    )
