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
    (
        "/projects",
        "Projects",
        "Selected builds, case studies, and shipped work",
    ),
    (
        "/certifications",
        "Certifications",
        "Professional learning and accredited achievements",
    ),
    (
        "/cv",
        "CV",
        "Experience, education, and a downloadable resume",
    ),
    (
        "/interests/",
        "Interests",
        "The topics, hobbies, and ideas behind the work",
    ),
    (
        "/contact",
        "Contact",
        "Ways to get in touch and start a conversation",
    ),
]

CONTACT_LINKS = [
    (
        "/contact",
        "Email Me",
        "Use the contact form",
    ),
    (
        "https://www.linkedin.com/in/mackenzie-blackaby-884b16217/",
        "LinkedIn",
        "Professional profile",
    ),
    (
        "https://github.com/MackenzieBlackaby",
        "GitHub",
        "Code and projects",
    ),
]

SCRIPT_SRCS = {
    "fade": "/scripts/fade.js",
    "resetScroll": "/scripts/resetScroll.js",
    "menuToggle": "/scripts/menuToggle.js",
    "contactFormFeedback": "/scripts/contactFormFeedback.js",
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


def output_to_route(output: str) -> str:
    normalized = output.replace("\\", "/")
    if normalized == "index.html":
        return "/"
    if normalized.endswith("/index.html"):
        normalized = normalized[:-10]
    elif normalized.endswith(".html"):
        normalized = normalized[:-5]
    return "/" + normalized.lstrip("/")


def normalize_route(route: str) -> str:
    if route == "/":
        return route
    return route.rstrip("/")


def nav_item_is_current(
    page_output: str, href: str
) -> bool:
    current = normalize_route(
        output_to_route(page_output)
    )
    target = normalize_route(href)
    return current == target or (
        target != "/"
        and current.startswith(target + "/")
    )


def render_header(page: dict) -> str:
    links = []
    for href, label, meta in NAV_ITEMS:
        current_attr = ""
        if nav_item_is_current(page["output"], href):
            current_attr = (
                ' aria-current="page"'
            )
        links.extend(
            [
                "                <a"
                f' href="{href}"{current_attr}',
                "                >",
                '                    <span class="navLinkCopy">',
                f'                        <span class="navLinkLabel">{label}</span>',
                f'                        <span class="navLinkMeta">{meta}</span>',
                "                    </span>",
                "                </a>",
            ]
        )
    nav = "\n".join(links)
    return "\n".join(
        [
            "            <header id=\"header\">",
            "                <div class=\"logo\">",
            '                    <a href="/" aria-label="Home">MB</a>',
            "                </div>",
            "                <button",
            "                    class=\"menuToggle\"",
            "                    id=\"menuToggle\"",
            '                    type="button"',
            '                    aria-controls="navLinks"',
            '                    aria-expanded="false"',
            '                    aria-label="Open navigation menu"',
            "                >",
            '                    <span class="menuToggleText" id="menuToggleLabel">Menu</span>',
            '                    <span class="menuToggleIcon" aria-hidden="true">',
            "                        <span></span>",
            "                        <span></span>",
            "                        <span></span>",
            "                    </span>",
            "                </button>",
            "                <button",
            "                    class=\"menuBackdrop\"",
            "                    id=\"menuBackdrop\"",
            '                    type="button"',
            '                    aria-label="Close navigation menu"',
            "                    hidden",
            "                >",
            "                </button>",
            "                <nav",
            "                    class=\"nav-links\"",
            "                    id=\"navLinks\"",
            '                    aria-label="Primary navigation"',
            "                >",
            '                    <div class="nav-linksIntro">',
            '                        <p class="navLinksEyebrow">Navigation</p>',
            '                        <p class="navLinksTitle">Choose a section</p>',
            "                    </div>",
            nav,
            "                </nav>",
            "            </header>",
        ]
    )


def render_footer(note: str) -> str:
    contact_links = []
    for href, label, description in CONTACT_LINKS:
        attrs = [f'href="{href}"']
        if href.startswith("http"):
            attrs.append('target="_blank"')
            attrs.append(
                'rel="noopener noreferrer"'
            )
        attrs.append(
            'class="footerContactLink"'
        )
        contact_links.extend(
            [
                f"                    <a {' '.join(attrs)}>",
                f"                <span>{label}</span>",
                f"                <small>{description}</small>",
                "                    </a>",
            ]
        )
    return "\n".join(
        [
            "        <footer>",
            '            <div class="footerContactBand">',
            '                <p class="footerContactTitle">',
            "                    Get in touch",
            "                </p>",
            '                <div class="footerContactLinks">',
            *contact_links,
            "                </div>",
            "            </div>",
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
        "{{header}}": render_header(page),
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
