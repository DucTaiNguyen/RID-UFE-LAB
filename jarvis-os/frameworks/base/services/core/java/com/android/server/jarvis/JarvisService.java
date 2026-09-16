package com.android.server.jarvis;

import android.content.Context;

import com.jarvis.os.intent.IntentContract;

public class JarvisService {

    private final Context mContext;

    private final IntentManager mIntentManager;
    private final PolicyManager mPolicyManager;
    private final ToolRegistry mToolRegistry;
    private final MemoryManager mMemoryManager;
    private final TraceEngine mTraceEngine;

    public JarvisService(Context context) {
        mContext = context;

        mIntentManager = new IntentManager();
        mPolicyManager = new PolicyManager();
        mToolRegistry = new ToolRegistry();
        mMemoryManager = new MemoryManager();
        mTraceEngine = new TraceEngine();

        mToolRegistry.register(
                new AppTool(context)
        );
    }

    public String ask(String input) {

        String traceId =
                mTraceEngine.newTraceId();

        IntentContract intent =
                mIntentManager.parse(input);

        int policy =
                mPolicyManager.evaluate(intent);

        if (policy == PolicyDecision.DENY) {

            ObservationRecord observation =
                    new ObservationRecord(
                            "POLICY_DENY",
                            intent.getTarget(),
                            false,
                            0,
                            "Execution denied by policy"
                    );

            recordTrace(
                    traceId,
                    input,
                    intent,
                    policy,
                    observation
            );

            return buildResponse(
                    traceId,
                    intent,
                    policy,
                    observation
            );
        }

        if (policy == PolicyDecision.REQUIRE_CONFIRMATION) {

            ObservationRecord observation =
                    new ObservationRecord(
                            "CONFIRMATION_REQUIRED",
                            intent.getTarget(),
                            false,
                            0,
                            "User confirmation required"
                    );

            recordTrace(
                    traceId,
                    input,
                    intent,
                    policy,
                    observation
            );

            return buildResponse(
                    traceId,
                    intent,
                    policy,
                    observation
            );
        }

        long startNs =
                System.nanoTime();

        ToolResult result =
                mToolRegistry.execute(intent);

        long latencyMs =
                (System.nanoTime() - startNs)
                        / 1_000_000L;

        ObservationRecord observation =
                new ObservationRecord(
                        "EXECUTE",
                        intent.getTarget(),
                        result.isSuccess(),
                        latencyMs,
                        result.getMessage()
                );

        recordTrace(
                traceId,
                input,
                intent,
                policy,
                observation
        );

        return buildResponse(
                traceId,
                intent,
                policy,
                observation
        );
    }

    private void recordTrace(
            String traceId,
            String input,
            IntentContract intent,
            int policy,
            ObservationRecord observation) {

        TraceRecord trace =
                new TraceRecord(
                        traceId,
                        input,
                        String.valueOf(intent.getType()),
                        intent.getTarget(),
                        policy,
                        observation.getAction(),
                        observation.isSuccess(),
                        observation.getLatencyMs(),
                        observation.getMessage()
                );

        mTraceEngine.record(trace);

        rememberObservation(observation);
    }

    private void rememberObservation(
            ObservationRecord observation) {

        String value =
                "action=" + observation.getAction()
                        + ";target=" + observation.getTarget()
                        + ";success=" + observation.isSuccess()
                        + ";latencyMs=" + observation.getLatencyMs()
                        + ";message=" + observation.getMessage();

        MemoryRecord record =
                new MemoryRecord(
                        MemoryRecord.EPISODIC,
                        MemoryRecord.PRIVATE,
                        "jarvis.execution",
                        value
                );

        mMemoryManager.remember(record);
    }

    private String buildResponse(
            String traceId,
            IntentContract intent,
            int policy,
            ObservationRecord observation) {

        return "traceId=" + traceId
                + ";intent=" + intent.getType()
                + ";target=" + intent.getTarget()
                + ";policy=" + policy
                + ";action=" + observation.getAction()
                + ";success=" + observation.isSuccess()
                + ";latencyMs=" + observation.getLatencyMs()
                + ";message=" + observation.getMessage();
    }

    public int memorySize() {
        return mMemoryManager.size();
    }

    public int traceSize() {
        return mTraceEngine.size();
    }

    public String state() {
        return "JARVIS_OS_READY";
    }
}
