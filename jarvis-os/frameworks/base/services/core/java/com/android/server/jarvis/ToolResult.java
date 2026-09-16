package com.android.server.jarvis;

public final class ToolResult {

    private final boolean success;
    private final String message;

    public ToolResult(boolean success, String message) {
        this.success = success;
        this.message = message;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getMessage() {
        return message;
    }

    @Override
    public String toString() {
        return "ToolResult{" +
                "success=" + success +
                ", message='" + message + '\'' +
                '}';
    }
}
