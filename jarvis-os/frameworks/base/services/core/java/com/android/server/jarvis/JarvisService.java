package com.android.server.jarvis;

import com.jarvis.os.intent.IntentContract;

public final class JarvisService {

    private final IntentManager intentManager;

    public JarvisService() {
        intentManager = new IntentManager();
    }

    public IntentContract process(String input) {
        return intentManager.parse(input);
    }
}
