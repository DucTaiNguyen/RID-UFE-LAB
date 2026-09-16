package com.android.server.jarvis;

import android.content.Context;

import com.jarvis.os.IJarvisService;
import com.jarvis.os.intent.IntentContract;

public final class JarvisService extends IJarvisService.Stub {

    private final Context mContext;
    private final IntentManager mIntentManager;

    public JarvisService(Context context) {
        mContext = context;
        mIntentManager = new IntentManager();
    }

    @Override
    public String ask(String input) {
        IntentContract intent = mIntentManager.parse(input);
        return intent.toString();
    }

    @Override
    public String state() {
        return "JARVIS_OS_READY";
    }
}
