package com.android.server.jarvis;

public final class MemoryRecord {

    public static final String WORKING = "WORKING";
    public static final String EPISODIC = "EPISODIC";
    public static final String SEMANTIC = "SEMANTIC";
    public static final String PREFERENCE = "PREFERENCE";

    public static final String PUBLIC = "PUBLIC";
    public static final String PRIVATE = "PRIVATE";
    public static final String SENSITIVE = "SENSITIVE";
    public static final String SYSTEM = "SYSTEM";

    private final String type;
    private final String sensitivity;
    private final String key;
    private final String value;
    private final long timestampMs;

    public MemoryRecord(
            String type,
            String sensitivity,
            String key,
            String value) {

        this.type = type;
        this.sensitivity = sensitivity;
        this.key = key;
        this.value = value;
        this.timestampMs = System.currentTimeMillis();
    }

    public String getType() {
        return type;
    }

    public String getSensitivity() {
        return sensitivity;
    }

    public String getKey() {
        return key;
    }

    public String getValue() {
        return value;
    }

    public long getTimestampMs() {
        return timestampMs;
    }
}
