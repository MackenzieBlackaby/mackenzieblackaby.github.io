const menuToggle =
    document.getElementById(
        "menuToggle"
    );
const navLinks =
    document.getElementById("navLinks");
const header =
    document.getElementById("header");

if (menuToggle && navLinks && header) {
    const mobileMedia =
        window.matchMedia(
            "(max-width: 767px)"
        );

    const setMenuState = (isOpen) => {
        navLinks.classList.toggle(
            "show",
            isOpen
        );
        navLinks.hidden =
            mobileMedia.matches && !isOpen;
        menuToggle.classList.toggle(
            "rotated",
            isOpen
        );
        header.classList.toggle(
            "headerExpanded",
            isOpen
        );
        menuToggle.setAttribute(
            "aria-expanded",
            String(isOpen)
        );
        menuToggle.setAttribute(
            "aria-label",
            isOpen
                ? "Close navigation menu"
                : "Open navigation menu"
        );
    };

    const syncMenuForViewport = () => {
        if (!mobileMedia.matches) {
            navLinks.hidden = false;
            setMenuState(false);
            return;
        }

        if (!navLinks.classList.contains("show")) {
            navLinks.hidden = true;
            menuToggle.setAttribute(
                "aria-expanded",
                "false"
            );
            menuToggle.setAttribute(
                "aria-label",
                "Open navigation menu"
            );
        }
    };

    menuToggle.addEventListener(
        "click",
        () => {
            setMenuState(
                !navLinks.classList.contains(
                    "show"
                )
            );
        }
    );

    navLinks
        .querySelectorAll("a")
        .forEach((link) => {
            link.addEventListener(
                "click",
                () => {
                    if (
                        mobileMedia.matches
                    ) {
                        setMenuState(false);
                    }
                }
            );
        });

    document.addEventListener(
        "keydown",
        (event) => {
            if (
                event.key === "Escape" &&
                navLinks.classList.contains(
                    "show"
                )
            ) {
                setMenuState(false);
                menuToggle.focus();
            }
        }
    );

    mobileMedia.addEventListener(
        "change",
        syncMenuForViewport
    );

    syncMenuForViewport();
}
