package com.android.server.jarvis;

import com.jarvis.os.intent.IntentContract;

import java.util.ArrayList;
import java.util.List;

public final class ToolRegistry {

    private final List<JarvisTool> tools = new ArrayList<>();

    public void register(JarvisTool tool) {
        if (tool != null) {
            tools.add(tool);
        }
    }

    public ToolResult execute(IntentContract intent) {

        if (intent == null) {
            return new ToolResult(false, "Null intent");
        }

        for (JarvisTool tool : tools) {
            if (tool.supports(intent)) {
                return tool.execute(intent);
            }
        }

        return new ToolResult(
                false,
                "No tool supports intent"
        );
    }
}
