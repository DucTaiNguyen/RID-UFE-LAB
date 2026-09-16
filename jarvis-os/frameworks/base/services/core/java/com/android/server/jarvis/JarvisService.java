package com.android.server.jarvis;

import android.content.Context;

import com.jarvis.os.IJarvisService;
import com.jarvis.os.intent.IntentContract;

public final class JarvisService extends IJarvisService.Stub {

    private final Context mContext;
    private final IntentManager mIntentManager;
    private final PolicyManager mPolicyManager;
    private final ToolRegistry mToolRegistry;

    public JarvisService(Context context) {
        mContext = context;

        mIntentManager = new IntentManager();
        mPolicyManager = new PolicyManager();

        mToolRegistry = new ToolRegistry();
        mToolRegistry.register(new AppTool(context));
    }

    @Override
    public String ask(String input) {

        // 1. Parse user input
        IntentContract intent =
                mIntentManager.parse(input);

        // 2. Evaluate security policy
        PolicyDecision decision =
                mPolicyManager.evaluate(intent);

        // 3. Block denied actions
        if (decision.getDecision()
                == PolicyDecision.DENY) {

            return "DENIED: "
                    + decision.getReason();
        }

        // 4. Require confirmation for high-risk actions
        if (decision.getDecision()
                == PolicyDecision.REQUIRE_CONFIRMATION) {

            return "CONFIRMATION_REQUIRED: "
                    + decision.getReason();
        }

        // 5. Execute only after ALLOW
        ToolResult result =
                mToolRegistry.execute(intent);

        return "intent=" + intent
                + ", policy=" + decision
                + ", result=" + result;
    }

    @Override
    public String state() {
        return "JARVIS_OS_READY";
    }
}
