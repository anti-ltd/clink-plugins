# ---
# name: NuKey Themes
# icon: square.grid.2x2
# summary: Browse themes shared from NuKey and bring them into Clink
# version: 1.0
# author: Clink
# network: nukey-themes.ske-d03.workers.dev
# ---

# A page in the app that browses the NuKey theme gallery.
#
# The gallery is one JSON list (every share, newest first), so searching,
# sorting and paging all happen here: the list is fetched once when the page
# opens and again from the refresh button or pull to refresh. It lives in "_shares", working memory
# that is never saved, so the plugin's saved state is only the layout and sort
# the person chose. Downloading hands the .nukeytheme to Clink's own NuKey
# import sheet, where the person confirms before anything is saved.

GALLERY = "https://nukey-themes.ske-d03.workers.dev/gallery"
BATCH = 20
SORTS = ["Newest", "Popular", "Liked"]


def initial():
    return {"layout": "grid", "sort": "Newest", "_shares": [], "_loading": False,
            "_error": None, "_shown": BATCH, "_query": ""}


def pages(state):
    return [page("browse", "NuKey Themes", icon="square.grid.2x2",
                 summary="Themes people share from NuKey", anchor="themes.theme"),
            page("theme", "Theme", listed=False)]


def load(state):
    state["_loading"] = True
    state["_error"] = None
    fetch("gallery", GALLERY)


def on_page(id, params, state):
    # Once per session: coming back to the list keeps what it had.
    if id == "browse" and not state["_shares"] and not state["_loading"]:
        load(state)
    return state


def on_response(id, response, state):
    if id != "gallery":
        return state
    state["_loading"] = False
    data = response["data"]
    if not response["ok"] or not data or not data.get("success"):
        state["_error"] = response["error"] or "The gallery didn't answer"
        return state
    state["_error"] = None
    state["_shares"] = [s for s in data.get("shares", []) if s.get("download_url") and s.get("preview_url")]
    state["_shown"] = BATCH
    return state


def visible(state):
    query = state["_query"].strip().lower()
    shares = state["_shares"]
    if query:
        shares = [s for s in shares if query in s.get("name", "").lower() or query in s.get("author", "").lower()]
    if state["sort"] == "Popular":
        shares = sorted(shares, key=lambda s: -s.get("downloads", 0))
    elif state["sort"] == "Liked":
        shares = sorted(shares, key=lambda s: -s.get("likes", 0))
    return shares


def count(n):
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def stats(share):
    return hstack([icon("arrow.down.circle", size=13, color="gray"), text(count(share.get("downloads", 0)), size=13),
                   icon("heart", size=13, color="gray"), text(count(share.get("likes", 0)), size=13)],
                  spacing=4, align="center")


def cell(share):
    return tile([
        image(share["preview_url"], aspect=1.6, radius=10, action="open", value=share),
        text(share.get("name", ""), size=16, weight="semibold", lines=1),
        text("by " + share.get("author", "?"), size=13, lines=1),
        hstack([stats(share), spacer(), button("", action="get", value=share["download_url"],
                                               icon="arrow.down.circle.fill", style="primary")], spacing=6),
    ], spacing=6, padding=10)


def row(share):
    return tile([hstack([
        image(share["preview_url"], width=112, aspect=1.6, radius=8, action="open", value=share),
        vstack([text(share.get("name", ""), size=16, weight="semibold", lines=2),
                text("by " + share.get("author", "?"), size=13, lines=1),
                stats(share)], spacing=4),
        spacer(),
        button("", action="get", value=share["download_url"], icon="arrow.down.circle.fill", style="primary"),
    ], spacing=12)], padding=10)


def browse(state):
    toolbar = [button("", action="reload", icon="arrow.clockwise", enabled=not state["_loading"]),
               button("", action="layout", icon="list.bullet" if state["layout"] == "grid" else "square.grid.2x2")]
    body = [segmented(SORTS, value=state["sort"], key="sort")]
    shares = visible(state)
    # A refresh keeps the list it has on screen until the new one arrives.
    if state["_shares"]:
        if state["_loading"]:
            body.append(spinner("Refreshing"))
        elif state["_error"]:
            body.append(text("Couldn't refresh: " + state["_error"], size=13, color="orange"))
    if state["_loading"] and not state["_shares"]:
        body.append(spinner("Loading themes"))
    elif state["_error"] and not state["_shares"]:
        body.append(empty("Couldn't load themes", state["_error"], icon="wifi.slash", action="reload", label="Try again"))
    elif not shares:
        if state["_query"]:
            body.append(empty("No matches", "Nothing called \"" + state["_query"] + "\"", icon="magnifyingglass"))
        else:
            body.append(empty("No themes yet", "Pull down to check again", icon="square.grid.2x2"))
    else:
        shown = shares[:state["_shown"]]
        if state["layout"] == "grid":
            body.append(grid([cell(s) for s in shown], columns=2, spacing=12))
        else:
            body.append(vstack([row(s) for s in shown], spacing=10))
        if len(shares) > len(shown):
            body.append(loader("more", value=len(shown)))
        else:
            body.append(text("1 theme" if len(shares) == 1 else f"{len(shares)} themes", size=13, align="center"))
    return screen(body, title="NuKey Themes", search="_query", search_placeholder="Search themes or authors",
                  toolbar=toolbar, refresh="reload")


def detail(share):
    when = share.get("created_at", "")[:10]
    return screen([
        image(share["preview_url"], aspect=1.6, radius=14, fit="fit"),
        text(share.get("name", ""), size=24, weight="bold"),
        text("by " + share.get("author", "?") + ("  ·  " + when if when else ""), size=14),
        stats(share),
        spacer(8),
        button("Download", action="get", value=share["download_url"], icon="arrow.down.circle.fill", style="primary"),
        text("Clink shows the theme before adding it to your themes.", size=13),
    ], title=share.get("name", "Theme"))


def page_view(id, params, state):
    if id == "theme" and params.get("preview_url"):
        return detail(params)
    return browse(state)


def on_action(action, value, state):
    if action == "reload":
        load(state)
    elif action == "more" and not state["_loading"]:
        state["_shown"] = max(state["_shown"], value + BATCH)
    elif action == "layout":
        state["layout"] = "list" if state["layout"] == "grid" else "grid"
    elif action == "open":
        navigate("theme", value)
    elif action == "get":
        import_theme(value, format="nukey")
    return state
