package com.android.server.jarvis;

public final class TraceRecord {

    private final String traceId;
    private final String input;
    private final String intentType;
    private final String target;
    private final int policyDecision;
    private final String action;
    private final boolean success;
    private final long latencyMs;
    private final String message;
    private final long timestampMs;

    public TraceRecord(
            String traceId,
            String input,
            String intentType,
            String target,
            int policyDecision,
            String action,
            boolean success,
            long latencyMs,
            String message) {

        this.traceId = traceId;
        this.input = input;
        this.intentType = intentType;
        this.target = target;
        this.policyDecision = policyDecision;
        this.action = action;
        this.success = success;
        this.latencyMs = latencyMs;
        this.message = message;
        this.timestampMs = System.currentTimeMillis();
    }

    public String getTraceId() {
        return traceId;
    }

    public String getInput() {
        return input;
    }

    public String getIntentType() {
        return intentType;
    }

    public String getTarget() {
        return target;
    }

    public int getPolicyDecision() {
        return policyDecision;
    }

    public String getAction() {
        return action;
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
        return "TraceRecord{" +
                "traceId='" + traceId + '\'' +
                ", input='" + input + '\'' +
                ", intentType='" + intentType + '\'' +
                ", target='" + target + '\'' +
                ", policyDecision=" + policyDecision +
                ", action='" + action + '\'' +
                ", success=" + success +
                ", latencyMs=" + latencyMs +
                ", message='" + message + '\'' +
                ", timestampMs=" + timestampMs +
                '}';
    }
}
