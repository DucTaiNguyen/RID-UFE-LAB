package com.android.server.jarvis;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;

import com.jarvis.os.intent.IntentContract;

public final class AppTool implements JarvisTool {

    private final Context context;

    public AppTool(Context context) {
        this.context = context;
    }

    @Override
    public String getName() {
        return "AppTool";
    }

    @Override
    public boolean supports(IntentContract intent) {
        return intent != null
                && intent.getType() == IntentContract.OPEN_APP;
    }

    @Override
    public ToolResult execute(IntentContract intent) {

        if (!supports(intent)) {
            return new ToolResult(
                    false,
                    "Unsupported intent"
            );
        }

        String target = intent.getTarget();

        String packageName = resolvePackage(target);

        if (packageName == null) {
            return new ToolResult(
                    false,
                    "Application not found: " + target
            );
        }

        PackageManager pm = context.getPackageManager();

        Intent launchIntent =
                pm.getLaunchIntentForPackage(packageName);

        if (launchIntent == null) {
            return new ToolResult(
                    false,
                    "Application cannot be launched: "
                            + packageName
            );
        }

        launchIntent.addFlags(
                Intent.FLAG_ACTIVITY_NEW_TASK
        );

        context.startActivity(launchIntent);

        return new ToolResult(
                true,
                "Application launched: " + packageName
        );
    }

    private String resolvePackage(String target) {

        if ("camera".equalsIgnoreCase(target)) {
            return "com.android.camera2";
        }

        if ("chrome".equalsIgnoreCase(target)) {
            return "com.android.chrome";
        }

        return null;
    }
}
