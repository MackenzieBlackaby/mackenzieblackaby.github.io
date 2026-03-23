const fadeTargets =
    document.querySelectorAll(
        ".fadeIn"
    );

const reveal = (element) => {
    element.classList.add("animate");
};

if (
    window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches ||
    !(
        "IntersectionObserver" in
        window
    )
) {
    fadeTargets.forEach(reveal);
} else {
    const observer =
        new IntersectionObserver(
            (entries) => {
                entries.forEach(
                    (entry) => {
                        if (
                            entry.isIntersecting
                        ) {
                            reveal(
                                entry.target
                            );
                            observer.unobserve(
                                entry.target
                            );
                        }
                    }
                );
            },
            {
                threshold: 0.02,
                rootMargin:
                    "0px 0px -8% 0px",
            }
        );

    fadeTargets.forEach((el) => {
        observer.observe(el);
    });
}
