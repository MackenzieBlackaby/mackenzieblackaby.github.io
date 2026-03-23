from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "site_src"
LAYOUT = (SRC / "layout.html").read_text(
    encoding="utf-8"
)
PAGES = json.loads(
    (SRC / "pages.json").read_text(
        encoding="utf-8"
    )
)

NAV_ITEMS = [
    ("/projects", "Projects"),
    ("/certifications", "Certifications"),
    ("/cv", "CV"),
    ("/interests/", "Interests"),
    ("/contact", "Contact"),
]

SCRIPT_SRCS = {
    "fade": "/scripts/fade.js",
    "resetScroll": "/scripts/resetScroll.js",
    "menuToggle": "/scripts/menuToggle.js",
}


def render_meta(page: dict) -> str:
    description = page.get("description", "")
    image = page.get(
        "image", "/Resources/Images/ico512.png"
    )
    url = canonical_url(page["output"])
    meta_type = page.get("type", "website")

    lines = [
        "        <meta",
        '            property="og:title"',
        f'            content="{escape_attr(page["title"])}"',
        "        />",
        "        <meta",
        '            property="og:description"',
        f'            content="{escape_attr(description)}"',
        "        />",
        "        <meta",
        '            property="og:image"',
        f'            content="{escape_attr(image)}"',
        "        />",
        "        <meta",
        '            property="og:url"',
        f'            content="{escape_attr(url)}"',
        "        />",
        "        <meta",
        '            name="type"',
        f'            content="{escape_attr(meta_type)}"',
        "        />",
        "        <meta",
        '            name="twitter:card"',
        '            content="summary_large_image"',
        "        />",
        "        <meta",
        '            name="twitter:title"',
        f'            content="{escape_attr(page["title"])}"',
        "        />",
        "        <meta",
        '            name="twitter:description"',
        f'            content="{escape_attr(description)}"',
        "        />",
        "        <meta",
        '            name="twitter:image"',
        f'            content="{escape_attr(image)}"',
        "        />",
    ]
    return "\n".join(lines)


def canonical_url(output: str) -> str:
    normalized = output.replace("\\", "/")
    if normalized == "index.html":
        return "https://blackaby.uk"
    if normalized.endswith("/index.html"):
        normalized = normalized[:-10]
    elif normalized.endswith(".html"):
        normalized = normalized[:-5]
    return (
        "https://blackaby.uk/"
        + normalized.lstrip("/")
    )


def render_header() -> str:
    links = []
    for href, label in NAV_ITEMS:
        links.extend(
            [
                "                <a"
                f' href="{href}"',
                f"                    >{label}</a",
                "                >",
            ]
        )
    nav = "\n".join(links)
    return "\n".join(
        [
            "            <header id=\"header\">",
            "                <h1 class=\"logo\">",
            "                    <a href=\"/\">MB</a>",
            "                </h1>",
            "                <button",
            "                    class=\"menuToggle\"",
            "                    id=\"menuToggle\"",
            "                >",
            "                    &#9776;",
            "                </button>",
            "                <div",
            "                    class=\"nav-links\"",
            "                    id=\"navLinks\"",
            "                >",
            nav,
            "                </div>",
            "            </header>",
        ]
    )


def render_footer(note: str) -> str:
    return "\n".join(
        [
            "        <footer>",
            "            <p>",
            "                &copy; 2023 Mackenzie",
            "                Blackaby. All rights",
            "                reserved.",
            "            </p>",
            "            <br />",
            f"            {note}",
            "        </footer>",
        ]
    )


def render_scripts(page: dict) -> str:
    lines = []
    for key in page.get("scripts", []):
        src = SCRIPT_SRCS[key]
        lines.append(
            f'        <script src="{src}"></script>'
        )
    return "\n".join(lines)


def read_fragment(relative_path: str | None) -> str:
    if not relative_path:
        return ""
    path = SRC / relative_path
    return path.read_text(encoding="utf-8").rstrip()


def escape_attr(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render_page(page: dict) -> str:
    replacements = {
        "{{meta_tags}}": render_meta(page),
        "{{title}}": page["title"],
        "{{extra_head}}": "",
        "{{body_class_attr}}": (
            f' class="{page["body_class"]}"'
            if page.get("body_class")
            else ""
        ),
        "{{header}}": render_header(),
        "{{main_content}}": read_fragment(
            page["content"]
        ),
        "{{after_main_content}}": read_fragment(
            page.get("after_content")
        ),
        "{{footer}}": render_footer(
            page.get(
                "footer_note",
                "With hardship comes ease",
            )
        ),
        "{{script_tags}}": render_scripts(page),
    }

    rendered = LAYOUT
    for token, value in replacements.items():
        rendered = rendered.replace(token, value)
    return rendered + "\n"


def main() -> None:
    for page in PAGES:
        output_path = ROOT / page["output"]
        output_path.parent.mkdir(
            parents=True, exist_ok=True
        )
        output_path.write_text(
            render_page(page), encoding="utf-8"
        )
        print(f"Built {page['output']}")


if __name__ == "__main__":
    main()
