# ---
# name: Keyboard2
# icon: square.grid.2x2
# summary: Keyboard2
# version: 1.1
# author: Clink
# network: keyboard2.eu
# ---

import json

BASE = "https://keyboard2.eu/"
BATCH = 20

# Reuses the editorially reviewed shared catalogue.
LABELS = {'af': {'Download': 'Laai af', 'Retry': 'Probeer weer', 'More': 'Meer', 'Refresh': 'Verfris', 'No results': 'Geen resultate nie', 'Search': 'Soek', "Couldn't read that theme": 'Kon nie daardie tema lees nie'}, 'de': {'Download': 'Laden', 'Retry': 'Erneut versuchen', 'More': 'Mehr', 'Refresh': 'Aktualisieren', 'No results': 'Keine Ergebnisse', 'Search': 'Suchen', "Couldn't read that theme": 'Design konnte nicht gelesen werden'}, 'es': {'Download': 'Descargar', 'Retry': 'Reintentar', 'More': 'Más', 'Refresh': 'Actualizar', 'No results': 'Sin resultados', 'Search': 'Buscar', "Couldn't read that theme": 'No se pudo leer ese tema'}, 'et': {'Download': 'Laadi alla', 'Retry': 'Proovi uuesti', 'More': 'Rohkem', 'Refresh': 'Värskenda', 'No results': 'Tulemusi pole', 'Search': 'Otsi', "Couldn't read that theme": 'Teemat ei õnnestunud lugeda'}, 'fr': {'Download': 'Télécharger', 'Retry': 'Réessayer', 'More': 'Plus', 'Refresh': 'Actualiser', 'No results': 'Aucun résultat', 'Search': 'Rechercher', "Couldn't read that theme": 'Impossible de lire ce thème'}, 'hu': {'Download': 'Letöltés', 'Retry': 'Újrapróbálkozás', 'More': 'Több', 'Refresh': 'Frissítés', 'No results': 'Nincs találat', 'Search': 'Keresés', "Couldn't read that theme": 'A téma nem olvasható be'}, 'it': {'Download': 'Scarica', 'Retry': 'Riprova', 'More': 'Altro', 'Refresh': 'Aggiorna', 'No results': 'Nessun risultato', 'Search': 'Cerca', "Couldn't read that theme": 'Impossibile leggere il tema'}, 'ja': {'Download': 'ダウンロード', 'Retry': '再試行', 'More': '増やす', 'Refresh': '更新', 'No results': '結果がありません', 'Search': '検索', "Couldn't read that theme": 'テーマを読み込めませんでした'}, 'ko': {'Download': '다운로드', 'Retry': '다시 시도', 'More': '더 보기', 'Refresh': '새로고침', 'No results': '결과 없음', 'Search': '검색', "Couldn't read that theme": '테마를 읽을 수 없습니다'}, 'ms': {'Download': 'Muat turun', 'Retry': 'Cuba lagi', 'More': 'Lagi', 'Refresh': 'Muat semula', 'No results': 'Tiada hasil', 'Search': 'Cari', "Couldn't read that theme": 'Tema itu tidak dapat dibaca'}, 'pt': {'Download': 'Transferir', 'Retry': 'Tentar novamente', 'More': 'Mais', 'Refresh': 'Atualizar', 'No results': 'Sem resultados', 'Search': 'Pesquisar', "Couldn't read that theme": 'Não foi possível ler esse tema'}, 'ru': {'Download': 'Загрузить', 'Retry': 'Повторить', 'More': 'Больше', 'Refresh': 'Обновить', 'No results': 'Ничего не найдено', 'Search': 'Поиск', "Couldn't read that theme": 'Не удалось прочитать тему'}, 'zh-Hans': {'Download': '下载', 'Retry': '重试', 'More': '更多', 'Refresh': '刷新', 'No results': '无结果', 'Search': '搜索', "Couldn't read that theme": '无法读取该主题'}, 'ro': {'Download': 'Descărcați', 'Retry': 'Reîncercați', 'More': 'Mai mult', 'Refresh': 'Reîmprospătează', 'No results': 'Niciun rezultat', 'Search': 'Caută', "Couldn't read that theme": 'Nu am putut citi acea tema'}, 'nl': {'Download': 'Downloaden', 'Retry': 'Opnieuw proberen', 'More': 'Meer', 'Refresh': 'Vernieuwen', 'No results': 'Geen resultaten', 'Search': 'Zoeken', "Couldn't read that theme": 'Ik kon dat thema niet lezen'}, 'zh-Hant': {'Download': '下載', 'Retry': '重試', 'More': '更多', 'Refresh': '重新整理', 'No results': '無結果', 'Search': '搜尋', "Couldn't read that theme": '無法讀取該主題'}, 'pl': {'Download': 'Pobierz', 'Retry': 'Spróbuj ponownie', 'More': 'Więcej', 'Refresh': 'Odśwież', 'No results': 'Brak wyników', 'Search': 'Szukaj', "Couldn't read that theme": 'Nie udało mi się przeczytać tego tematu'}, 'uk': {'Download': 'Завантажити', 'Retry': 'Повторіть спробу', 'More': 'більше', 'Refresh': 'Оновити', 'No results': 'Результатів немає', 'Search': 'Пошук', "Couldn't read that theme": 'Не вдалося прочитати цю тему'}, 'tr': {'Download': 'İndir', 'Retry': 'Yeniden dene', 'More': 'Daha Fazla', 'Refresh': 'Yenile', 'No results': 'Sonuç yok', 'Search': 'Ara', "Couldn't read that theme": 'Bu temayı okuyamadım'}, 'cs': {'Download': 'Stáhnout', 'Retry': 'Zkuste to znovu', 'More': 'více', 'Refresh': 'Obnovit', 'No results': 'Žádné výsledky', 'Search': 'Hledat', "Couldn't read that theme": 'Toto téma se nepodařilo přečíst'}, 'sk': {'Download': 'Stiahnuť', 'Retry': 'Skúste to znova', 'More': 'Viac', 'Refresh': 'Obnoviť', 'No results': 'Žiadne výsledky', 'Search': 'Hľadať', "Couldn't read that theme": 'Nepodarilo sa prečítať túto tému'}, 'el': {'Download': 'Λήψη', 'Retry': 'Επανάληψη', 'More': 'Περισσότερα', 'Refresh': 'Ανανέωση', 'No results': 'Κανένα αποτέλεσμα', 'Search': 'Αναζήτηση', "Couldn't read that theme": 'Δεν μπορούσα να διαβάσω αυτό το θέμα'}, 'sv': {'Download': 'Ladda ner', 'Retry': 'Försök igen', 'More': 'Mer', 'Refresh': 'Uppdatera', 'No results': 'Inga resultat', 'Search': 'Sök', "Couldn't read that theme": 'Kunde inte läsa det temat'}, 'da': {'Download': 'Download', 'Retry': 'Prøv igen', 'More': 'Mere', 'Refresh': 'Opdater', 'No results': 'Ingen resultater', 'Search': 'Søg', "Couldn't read that theme": 'Kunne ikke læse det tema'}, 'nb': {'Download': 'Last ned', 'Retry': 'Prøv på nytt', 'More': 'Mer', 'Refresh': 'Oppdater', 'No results': 'Ingen resultater', 'Search': 'Søk', "Couldn't read that theme": 'Kunne ikke lese det temaet'}, 'fi': {'Download': 'Lataa', 'Retry': 'Yritä uudelleen', 'More': 'Lisää', 'Refresh': 'Päivitä', 'No results': 'Ei tuloksia', 'Search': 'Hae', "Couldn't read that theme": 'En jaksanut lukea tuota teemaa'}, 'id': {'Download': 'Unduh', 'Retry': 'Coba lagi', 'More': 'Lebih lanjut', 'Refresh': 'Segarkan', 'No results': 'Tidak ada hasil', 'Search': 'Cari', "Couldn't read that theme": 'Tidak dapat membaca tema itu'}, 'vi': {'Download': 'Tải xuống', 'Retry': 'Thử lại', 'More': 'Thêm', 'Refresh': 'Làm mới', 'No results': 'Không có kết quả', 'Search': 'Tìm kiếm', "Couldn't read that theme": 'Không thể đọc chủ đề đó'}, 'en': {'Retry': 'Retry'}}


def initial():
    return {"_rows": [], "_loading": False, "_error": False, "_shown": BATCH, "_query": ""}


def label(key):
    locale = context()["locale"].replace("_", "-")
    return LABELS.get(locale, LABELS.get(locale.split("-")[0], {})).get(key, key)


def pages(state):
    return [page("browse", "Keyboard2", icon="square.grid.2x2", anchor="themes.theme")]


def load(state):
    state["_loading"] = True
    state["_error"] = False
    # The catalogue filename is content-hashed. Discover it on each refresh.
    fetch("index", BASE + "gallery", format="text")


def on_page(id, params, state):
    if not state["_rows"] and not state["_loading"]:
        load(state)
    return state


def valid_slug(slug):
    return isinstance(slug, str) and len(slug) > 0 and len(slug) < 160 and all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in slug)


def on_response(id, response, state):
    if id == "index":
        html = response.get("text") or ""
        marker = 'var DATA_URL = "'
        path = html.split(marker)[1].split('"')[0] if marker in html else ""
        if response["ok"] and path.startswith("themes/themes.") and path.endswith(".json") and ".." not in path and all(c in "abcdefghijklmnopqrstuvwxyz0123456789/.-" for c in path):
            fetch("catalogue", BASE + path)
        else:
            state["_loading"] = False
            state["_error"] = True
    elif id == "catalogue":
        state["_loading"] = False
        rows = response.get("data")
        if response["ok"] and isinstance(rows, list):
            state["_rows"] = [r for r in rows if isinstance(r, list) and len(r) >= 5 and valid_slug(r[0]) and isinstance(r[1], str)]
            state["_shown"] = BATCH
            state["_error"] = False
        else:
            state["_error"] = True
    return state


def cell(row):
    document = {"version": 1, "themes": json.loads(row[4])}
    photo = BASE + "themes/photos/" + row[0] + ".jpg" if row[3] == "photo" else ""
    return theme_card(row[1], document, format="keyboard2", photo_url=photo,
                      label=label("Download"), action="get", value=row[0])


def page_view(id, params, state):
    query = state["_query"].strip().lower()
    rows = [r for r in state["_rows"] if not query or query in (r[1] + " " + r[2] + " " + r[3] + " " + (r[5] if len(r) > 5 else "")).lower()]
    children = []
    if state["_loading"]:
        children.append(spinner())
    if state["_error"]:
        children.append(empty(label("Couldn't read that theme"), action="refresh", label=label("Retry"), icon="wifi.exclamationmark"))
    children.append(grid([cell(row) for row in rows[:state["_shown"]]], columns=1, spacing=12))
    if len(rows) > state["_shown"]:
        children.append(button(label("More"), action="more"))
    elif not rows and not state["_loading"] and not state["_error"]:
        children.append(empty(label("No results"), icon="magnifyingglass"))
    return screen(children, title="Keyboard2", search="_query", search_placeholder=label("Search"), search_action="search",
                  refresh="refresh", toolbar=[button(label("Refresh"), action="refresh", icon="arrow.clockwise")])


def on_action(action, value, state):
    if action == "refresh":
        load(state)
    elif action == "search":
        state["_query"] = value or ""
        state["_shown"] = BATCH
    elif action == "more":
        state["_shown"] = state["_shown"] + BATCH
    elif action == "get" and valid_slug(value):
        import_theme(BASE + "themes/files/" + value + ".keyboard2theme", format="keyboard2")
    return state
