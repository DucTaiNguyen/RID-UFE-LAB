package com.android.server.jarvis;

import com.jarvis.os.intent.IntentContract;

public interface JarvisTool {

    String getName();

    boolean supports(IntentContract intent);

    ToolResult execute(IntentContract intent);
}
