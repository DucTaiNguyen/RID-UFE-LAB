package com.android.server.jarvis;

import com.jarvis.os.intent.IntentContract;

public final class PolicyManager {

    public PolicyDecision evaluate(IntentContract intent) {

        if (intent == null) {
            return new PolicyDecision(
                    PolicyDecision.DENY,
                    "Null intent"
            );
        }

        switch (intent.getType()) {

            case IntentContract.OPEN_APP:
                return allow("Opening application");

            case IntentContract.SEARCH:
                return allow("Search operation");

            case IntentContract.SEND_MESSAGE:
                return confirmation("Messaging requires user confirmation");

            case IntentContract.SEND_EMAIL:
                return confirmation("Email requires user confirmation");

            case IntentContract.SYSTEM_SETTING:
                return confirmation("System setting change requires confirmation");

            case IntentContract.CLOSE_APP:
                return confirmation("Closing applications requires confirmation");

            case IntentContract.UNKNOWN:
            default:
                return deny("Unknown or unsupported intent");
        }
    }

    private PolicyDecision allow(String reason) {
        return new PolicyDecision(
                PolicyDecision.ALLOW,
                reason
        );
    }

    private PolicyDecision deny(String reason) {
        return new PolicyDecision(
                PolicyDecision.DENY,
                reason
        );
    }

    private PolicyDecision confirmation(String reason) {
        return new PolicyDecision(
                PolicyDecision.REQUIRE_CONFIRMATION,
                reason
        );
    }
}
