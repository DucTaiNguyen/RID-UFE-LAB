package com.jarvis.os.intent;

public final class IntentContract {

    public static final int OPEN_APP = 1;
    public static final int CLOSE_APP = 2;
    public static final int SEARCH = 3;
    public static final int SEND_MESSAGE = 4;
    public static final int SEND_EMAIL = 5;
    public static final int SYSTEM_SETTING = 6;
    public static final int UNKNOWN = 999;

    private final int type;
    private final String target;
    private final String payload;
    private final float confidence;
    private final boolean requiresConfirmation;

    public IntentContract(
            int type,
            String target,
            String payload,
            float confidence,
            boolean requiresConfirmation) {

        this.type = type;
        this.target = target;
        this.payload = payload;
        this.confidence = confidence;
        this.requiresConfirmation = requiresConfirmation;
    }

    public int getType() {
        return type;
    }

    public String getTarget() {
        return target;
    }

    public String getPayload() {
        return payload;
    }

    public float getConfidence() {
        return confidence;
    }

    public boolean requiresConfirmation() {
        return requiresConfirmation;
    }

    @Override
    public String toString() {
        return "IntentContract{" +
                "type=" + type +
                ", target='" + target + '\'' +
                ", payload='" + payload + '\'' +
                ", confidence=" + confidence +
                ", requiresConfirmation=" + requiresConfirmation +
                '}';
    }
}
