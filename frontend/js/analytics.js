const REGISTRATION_API = "/api/registrations";
const ANALYTICS_API = "/api/analytics/track";

function getSessionId() {
    let sessionId = sessionStorage.getItem("analytics_session_id");

    if (!sessionId) {
        sessionId =
            "SESSION-" +
            Date.now() +
            "-" +
            Math.random().toString(36).substring(2, 8);

        sessionStorage.setItem("analytics_session_id", sessionId);
    }

    return sessionId;
}

async function trackAnalytics(eventType, elementName) {
    const payload = {
        session_id: getSessionId(),
        event_type: eventType,
        page: window.location.pathname || "/",
        element: elementName,
        user_agent: navigator.userAgent
    };

    try {
        const response = await fetch(ANALYTICS_API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            console.error(
                "Analytics request failed:",
                response.status
            );
        }
    } catch (error) {
        console.error(
            "Analytics service unavailable:",
            error
        );
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Track page view
    trackAnalytics("page_view", "home-page");

    // Track clicks on register links
    document
        .querySelectorAll('a[href="#register"], .register-btn')
        .forEach((button) => {
            button.addEventListener("click", () => {
                trackAnalytics(
                    "register_click",
                    "register-button"
                );
            });
        });

    // Track video interactions
    document
        .querySelectorAll(
            'a[href*="youtube"], a[href*="vimeo"], video'
        )
        .forEach((videoElement) => {
            videoElement.addEventListener("click", () => {
                trackAnalytics(
                    "video_click",
                    "event-video"
                );
            });
        });

    // Track navigation section clicks
    document
        .querySelectorAll('a[href^="#"]')
        .forEach((link) => {
            link.addEventListener("click", () => {
                const target = link.getAttribute("href");

                if (target && target !== "#") {
                    trackAnalytics(
                        "section_view",
                        target.replace("#", "")
                    );
                }
            });
        });

    // Handle registration form submission
    const registrationForm =
        document.getElementById("registration-form");

    if (registrationForm) {
        registrationForm.addEventListener(
            "submit",
            async (event) => {
                event.preventDefault();

                const firstName =
                    document
                        .getElementById("firstname")
                        .value
                        .trim();

                const lastName =
                    document
                        .getElementById("lastname")
                        .value
                        .trim();

                const email =
                    document
                        .getElementById("email")
                        .value
                        .trim();

                const ticketCount = Number(
                    document
                        .getElementById("ticket-count")
                        .value
                );

                if (
                    !firstName ||
                    !lastName ||
                    !email ||
                    ticketCount < 1
                ) {
                    alert("Please complete all required fields.");
                    return;
                }

                const registrationPayload = {
                    event_id: 1,
                    attendee_name:
                        `${firstName} ${lastName}`,
                    email: email,
                    ticket_count: ticketCount
                };

                try {
                    const response = await fetch(
                        REGISTRATION_API,
                        {
                            method: "POST",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body: JSON.stringify(
                                registrationPayload
                            )
                        }
                    );

                    let result = {};

                    try {
                        result = await response.json();
                    } catch (jsonError) {
                        console.error(
                            "Invalid registration response:",
                            jsonError
                        );
                    }

                    if (!response.ok) {
                        console.error(
                            "Registration failed:",
                            result
                        );

                        const errorMessage =
                            typeof result.detail === "string"
                                ? result.detail
                                : "Registration failed.";

                        alert(errorMessage);
                        return;
                    }

                    await trackAnalytics(
                        "registration_completed",
                        "registration-form"
                    );

                    alert(
                        `Registration successful! Registration ID: ${result.id}`
                    );

                    registrationForm.reset();
                } catch (error) {
                    console.error(
                        "Registration service unavailable:",
                        error
                    );

                    alert(
                        "Registration service is unavailable. Please check whether the service is running."
                    );
                }
            }
        );
    }
});