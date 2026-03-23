const contactForm =
    document.querySelector(
        ".contactForm"
    );
const contactFormStatus =
    document.getElementById(
        "contactFormStatus"
    );

if (contactForm && contactFormStatus) {
    const fields = Array.from(
        contactForm.querySelectorAll(
            "input[required], textarea[required]"
        )
    );

    const setStatus = (
        message,
        isError = false
    ) => {
        contactFormStatus.textContent =
            message;
        contactFormStatus.classList.toggle(
            "isError",
            isError
        );
    };

    const updateFieldState = (
        field
    ) => {
        const invalid =
            !field.checkValidity();
        field.setAttribute(
            "aria-invalid",
            String(invalid)
        );
        return invalid;
    };

    fields.forEach((field) => {
        field.addEventListener(
            "blur",
            () => {
                updateFieldState(field);
            }
        );

        field.addEventListener(
            "input",
            () => {
                const invalid =
                    updateFieldState(
                        field
                    );
                if (
                    !invalid &&
                    contactFormStatus.classList.contains(
                        "isError"
                    )
                ) {
                    const hasErrors =
                        fields.some(
                            (item) =>
                                !item.checkValidity()
                        );
                    if (!hasErrors) {
                        setStatus("");
                    }
                }
            }
        );

        field.addEventListener(
            "invalid",
            () => {
                updateFieldState(field);
                setStatus(
                    "Please correct the highlighted fields before sending your message.",
                    true
                );
            }
        );
    });

    contactForm.addEventListener(
        "submit",
        (event) => {
            const invalidFields =
                fields.filter(
                    (field) =>
                        updateFieldState(
                            field
                        )
                );

            if (
                invalidFields.length > 0
            ) {
                event.preventDefault();
                setStatus(
                    "Please correct the highlighted fields before sending your message.",
                    true
                );
                invalidFields[0].focus();
                return;
            }

            setStatus(
                "Sending your message..."
            );
        }
    );
}
