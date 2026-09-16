package com.android.server.jarvis;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class MemoryManager {

    private final List<MemoryRecord> records =
            new ArrayList<>();

    public synchronized void remember(MemoryRecord record) {
        if (record == null) {
            return;
        }

        if (MemoryRecord.SENSITIVE.equals(
                record.getSensitivity())) {
            return;
        }

        records.add(record);
    }

    public synchronized List<MemoryRecord> recent(int limit) {

        if (limit <= 0 || records.isEmpty()) {
            return Collections.emptyList();
        }

        int fromIndex =
                Math.max(0, records.size() - limit);

        return new ArrayList<>(
                records.subList(fromIndex, records.size()));
    }

    public synchronized int size() {
        return records.size();
    }

    public synchronized void clear() {
        records.clear();
    }
}
