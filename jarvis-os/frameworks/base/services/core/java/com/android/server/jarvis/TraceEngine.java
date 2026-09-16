package com.android.server.jarvis;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

public final class TraceEngine {

    private final List<TraceRecord> traces =
            new ArrayList<>();

    public String newTraceId() {
        return UUID.randomUUID().toString();
    }

    public synchronized void record(TraceRecord trace) {
        if (trace == null) {
            return;
        }

        traces.add(trace);
    }

    public synchronized List<TraceRecord> recent(int limit) {

        if (limit <= 0 || traces.isEmpty()) {
            return Collections.emptyList();
        }

        int fromIndex =
                Math.max(0, traces.size() - limit);

        return new ArrayList<>(
                traces.subList(fromIndex, traces.size()));
    }

    public synchronized int size() {
        return traces.size();
    }

    public synchronized void clear() {
        traces.clear();
    }
}
