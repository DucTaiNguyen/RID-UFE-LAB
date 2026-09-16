package com.android.server.jarvis;

import android.content.Context;

import com.jarvis.os.IJarvisService;

public final class JarvisServiceManager {

    private JarvisServiceManager() {
    }

    public static IJarvisService create(Context context) {
        return new JarvisService(context);
    }
}
