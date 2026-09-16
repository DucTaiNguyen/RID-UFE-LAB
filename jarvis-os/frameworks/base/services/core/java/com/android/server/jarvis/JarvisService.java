package com.android.server.jarvis;

import android.content.Context;

import com.jarvis.os.intent.IntentContract;

public class JarvisService {

    private final Context mContext;

    private final IntentManager mIntentManager;
    private final PolicyManager mPolicyManager;
    private final ToolRegistry mToolRegistry;
    private final MemoryManager mMemoryManager;

    public JarvisService(Context context) {
        mContext = context;

        mIntentManager = new IntentManager();
        mPolicyManager = new PolicyManager();
        mToolRegistry = new ToolRegistry();
        mMemoryManager = new MemoryManager();

        mToolRegistry.register(
                new AppTool(context)
        );
    }

    public String ask(String input) {

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

            rememberObservation(observation);

            return new ExecutionTrace(
                    input,
                    String.valueOf(intent.getType()),
                    intent.getTarget(),
                    policy,
                    observation
            ).toString();
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

            rememberObservation(observation);

            return new ExecutionTrace(
                    input,
                    String.valueOf(intent.getType()),
                    intent.getTarget(),
                    policy,
                    observation
            ).toString();
        }

        long startNs =
                System.nanoTime();

        ToolResult result =
                mToolRegistry.execute(intent);

        long latencyMs =
                (System.nanoTime() - startNs) / 1_000_000L;

        ObservationRecord observation =
                new ObservationRecord(
                        "EXECUTE",
                        intent.getTarget(),
                        result.isSuccess(),
                        latencyMs,
                        result.getMessage()
                );

        rememberObservation(observation);

        return new ExecutionTrace(
                input,
                String.valueOf(intent.getType()),
                intent.getTarget(),
                policy,
                observation
        ).toString();
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

    public int memorySize() {
        return mMemoryManager.size();
    }

    public String state() {
        return "JARVIS_OS_READY";
    }
}
