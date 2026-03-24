const menuToggle =
    document.getElementById(
        "menuToggle"
    );
const menuToggleLabel =
    document.getElementById(
        "menuToggleLabel"
    );
const menuBackdrop =
    document.getElementById(
        "menuBackdrop"
    );
const navLinks =
    document.getElementById("navLinks");
const header =
    document.getElementById("header");

if (
    menuToggle &&
    navLinks &&
    header &&
    menuBackdrop
) {
    const mobileMedia =
        window.matchMedia(
            "(max-width: 767px)"
        );
    const focusableSelector =
        [
            "a[href]",
            "button:not([disabled])",
            "[tabindex]:not([tabindex='-1'])",
        ].join(", ");

    let lastFocusedElement = null;

    const isMenuOpen = () =>
        navLinks.classList.contains("show");

    const getFocusableElements =
        () =>
            [
                menuToggle,
                ...navLinks.querySelectorAll(
                    focusableSelector
                ),
            ].filter(
                (element) =>
                    !element.hasAttribute(
                        "disabled"
                    ) &&
                    !element.closest("[hidden]")
            );

    const updateMenuButtonCopy =
        (isOpen) => {
            if (!menuToggleLabel) {
                return;
            }

            menuToggleLabel.textContent =
                isOpen
                    ? "Close"
                    : "Menu";
        };

    const setMenuState = (
        isOpen,
        options = {}
    ) => {
        const {
            moveFocus = false,
            restoreFocus = true,
        } = options;
        const isMobile =
            mobileMedia.matches;
        const shouldOpen =
            isMobile && isOpen;

        if (
            shouldOpen &&
            restoreFocus &&
            document.activeElement instanceof
                HTMLElement
        ) {
            lastFocusedElement =
                document.activeElement;
        }

        navLinks.classList.toggle(
            "show",
            shouldOpen
        );
        navLinks.hidden =
            isMobile && !shouldOpen;

        menuBackdrop.classList.toggle(
            "show",
            shouldOpen
        );
        menuBackdrop.hidden =
            !shouldOpen;

        menuToggle.classList.toggle(
            "isOpen",
            shouldOpen
        );
        header.classList.toggle(
            "headerExpanded",
            shouldOpen
        );
        document.body.classList.toggle(
            "menuOpen",
            shouldOpen
        );

        menuToggle.setAttribute(
            "aria-expanded",
            String(shouldOpen)
        );
        menuToggle.setAttribute(
            "aria-label",
            shouldOpen
                ? "Close navigation menu"
                : "Open navigation menu"
        );
        updateMenuButtonCopy(
            shouldOpen
        );

        if (!shouldOpen) {
            if (
                restoreFocus &&
                lastFocusedElement &&
                lastFocusedElement.isConnected
            ) {
                const focusTarget =
                    lastFocusedElement;
                lastFocusedElement =
                    null;
                requestAnimationFrame(
                    () => {
                        focusTarget.focus();
                    }
                );
                return;
            }

            lastFocusedElement = null;
            return;
        }

        if (!moveFocus) {
            return;
        }

        requestAnimationFrame(() => {
            const focusableElements =
                getFocusableElements();
            const firstNavLink =
                focusableElements.find(
                    (element) =>
                        element !== menuToggle
                );

            (
                firstNavLink ||
                menuToggle
            ).focus();
        });
    };

    const syncMenuForViewport =
        () => {
            if (!mobileMedia.matches) {
                setMenuState(false, {
                    restoreFocus: false,
                });
                navLinks.hidden = false;
                return;
            }

            if (!isMenuOpen()) {
                navLinks.hidden = true;
                menuBackdrop.hidden =
                    true;
                menuBackdrop.classList.remove(
                    "show"
                );
                menuToggle.classList.remove(
                    "isOpen"
                );
                header.classList.remove(
                    "headerExpanded"
                );
                document.body.classList.remove(
                    "menuOpen"
                );
                menuToggle.setAttribute(
                    "aria-expanded",
                    "false"
                );
                menuToggle.setAttribute(
                    "aria-label",
                    "Open navigation menu"
                );
                updateMenuButtonCopy(
                    false
                );
            }
        };

    menuToggle.addEventListener(
        "click",
        () => {
            setMenuState(
                !isMenuOpen(),
                {
                    moveFocus: true,
                }
            );
        }
    );

    menuBackdrop.addEventListener(
        "click",
        () => {
            setMenuState(false);
            menuToggle.focus();
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
                        setMenuState(
                            false,
                            {
                                restoreFocus: false,
                            }
                        );
                    }
                }
            );
        });

    document.addEventListener(
        "keydown",
        (event) => {
            if (
                !mobileMedia.matches ||
                !isMenuOpen()
            ) {
                return;
            }

            if (
                event.key === "Escape"
            ) {
                setMenuState(false, {
                    restoreFocus: false,
                });
                menuToggle.focus();
                return;
            }

            if (event.key !== "Tab") {
                return;
            }

            const focusableElements =
                getFocusableElements();
            if (
                focusableElements.length ===
                0
            ) {
                return;
            }

            const firstElement =
                focusableElements[0];
            const lastElement =
                focusableElements[
                    focusableElements.length -
                        1
                ];

            if (
                event.shiftKey &&
                document.activeElement ===
                    firstElement
            ) {
                event.preventDefault();
                lastElement.focus();
            } else if (
                !event.shiftKey &&
                document.activeElement ===
                    lastElement
            ) {
                event.preventDefault();
                firstElement.focus();
            }
        }
    );

    mobileMedia.addEventListener(
        "change",
        syncMenuForViewport
    );

    syncMenuForViewport();
}
