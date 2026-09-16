package com.android.server.jarvis;

import android.content.Context;

import com.jarvis.os.IJarvisService;
import com.jarvis.os.intent.IntentContract;

public final class JarvisService extends IJarvisService.Stub {

    private final Context mContext;
    private final IntentManager mIntentManager;
    private final PolicyManager mPolicyManager;

    public JarvisService(Context context) {
        mContext = context;
        mIntentManager = new IntentManager();
        mPolicyManager = new PolicyManager();
    }

    @Override
    public String ask(String input) {

        IntentContract intent = mIntentManager.parse(input);

        PolicyDecision decision =
                mPolicyManager.evaluate(intent);

        return "intent=" + intent.toString()
                + ", policy=" + decision.toString();
    }

    @Override
    public String state() {
        return "JARVIS_OS_READY";
    }
}
