package com.android.server.jarvis;

public final class ObservationRecord {

    private final String action;
    private final String target;
    private final boolean success;
    private final long latencyMs;
    private final String message;
    private final long timestampMs;

    public ObservationRecord(
            String action,
            String target,
            boolean success,
            long latencyMs,
            String message) {

        this.action = action;
        this.target = target;
        this.success = success;
        this.latencyMs = latencyMs;
        this.message = message;
        this.timestampMs = System.currentTimeMillis();
    }

    public String getAction() {
        return action;
    }

    public String getTarget() {
        return target;
    }

    public boolean isSuccess() {
        return success;
    }

    public long getLatencyMs() {
        return latencyMs;
    }

    public String getMessage() {
        return message;
    }

    public long getTimestampMs() {
        return timestampMs;
    }

    @Override
    public String toString() {
        return "ObservationRecord{" +
                "action='" + action + '\'' +
                ", target='" + target + '\'' +
                ", success=" + success +
                ", latencyMs=" + latencyMs +
                ", message='" + message + '\'' +
                ", timestampMs=" + timestampMs +
                '}';
    }
}
