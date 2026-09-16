package com.android.server.jarvis;

import com.jarvis.os.intent.IntentContract;

import java.util.Locale;

public final class IntentManager {

    public IntentContract parse(String input) {

        if (input == null || input.trim().isEmpty()) {
            return unknown();
        }

        String text = input.trim().toLowerCase(Locale.ROOT);

        if (text.contains("mở camera")) {
            return new IntentContract(
                    IntentContract.OPEN_APP,
                    "camera",
                    "",
                    0.99f,
                    false
            );
        }

        if (text.contains("mở chrome")) {
            return new IntentContract(
                    IntentContract.OPEN_APP,
                    "chrome",
                    "",
                    0.99f,
                    false
            );
        }

        if (text.contains("gửi email")) {
            return new IntentContract(
                    IntentContract.SEND_EMAIL,
                    "email",
                    input,
                    0.95f,
                    true
            );
        }

        if (text.contains("gửi tin nhắn")) {
            return new IntentContract(
                    IntentContract.SEND_MESSAGE,
                    "messaging",
                    input,
                    0.95f,
                    true
            );
        }

        if (text.contains("tìm kiếm")) {
            return new IntentContract(
                    IntentContract.SEARCH,
                    "web",
                    input,
                    0.90f,
                    false
            );
        }

        return unknown();
    }

    private IntentContract unknown() {
        return new IntentContract(
                IntentContract.UNKNOWN,
                "",
                "",
                0.0f,
                true
        );
    }
}
