# JARVIS OS — SystemServer Integration v0.2

## Architecture

Android Boot
    |
    v
SystemServer
    |
    v
JarvisService
    |
    v
Binder / IJarvisService
    |
    +--> IntentManager
    |
    +--> PolicyManager
    |
    +--> ToolManager
    |
    +--> MemoryManager
    |
    +--> AgentRuntime

## Service lifecycle

1. SystemServer starts during Android framework initialization.
2. JarvisService is constructed with system Context.
3. The Binder implementation is registered with the system service manager.
4. Authorized framework clients obtain IJarvisService.
5. Requests are converted into structured IntentContract objects.
6. PolicyManager authorizes actions before execution.

## Security boundary

AI components must never receive unrestricted Binder, shell,
root, or arbitrary system privileges.

The intended path is:

AI
 -> Intent
 -> Policy
 -> Tool
 -> Android Framework

High-risk operations require explicit user confirmation.

## AOSP integration target

The eventual AOSP implementation will require:

- SystemServer registration
- Binder service publication
- framework API/build integration
- permission declaration
- signature-level access control
- SELinux policy
- CTS/unit/integration tests

This repository currently contains the architecture prototype.
Device-specific AOSP integration must be performed against a
specific supported AOSP device/branch.
