package com.android.server.jarvis;

public final class PolicyDecision {

    public static final int ALLOW = 0;
    public static final int DENY = 1;
    public static final int REQUIRE_CONFIRMATION = 2;

    private final int decision;
    private final String reason;

    public PolicyDecision(int decision, String reason) {
        this.decision = decision;
        this.reason = reason;
    }

    public int getDecision() {
        return decision;
    }

    public String getReason() {
        return reason;
    }

    public boolean isAllowed() {
        return decision == ALLOW;
    }

    public boolean requiresConfirmation() {
        return decision == REQUIRE_CONFIRMATION;
    }

    @Override
    public String toString() {
        return "PolicyDecision{" +
                "decision=" + decision +
                ", reason='" + reason + '\'' +
                '}';
    }
}
