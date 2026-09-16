package com.android.server.jarvis;

public final class ExecutionTrace {

    private final String input;
    private final String intentType;
    private final String target;
    private final int policyDecision;
    private final ObservationRecord observation;

    public ExecutionTrace(
            String input,
            String intentType,
            String target,
            int policyDecision,
            ObservationRecord observation) {

        this.input = input;
        this.intentType = intentType;
        this.target = target;
        this.policyDecision = policyDecision;
        this.observation = observation;
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

    public ObservationRecord getObservation() {
        return observation;
    }

    @Override
    public String toString() {
        return "ExecutionTrace{" +
                "input='" + input + '\'' +
                ", intentType='" + intentType + '\'' +
                ", target='" + target + '\'' +
                ", policyDecision=" + policyDecision +
                ", observation=" + observation +
                '}';
    }
}
