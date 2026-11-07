---
name: superpowers
description: Superpowers agent engineering skill suite (obra/superpowers) - Systematic debugging, test-driven development, verification-before-completion, clean code review, and deep root-cause analysis.
---

# Superpowers Engineering Skill Suite

Source: [https://github.com/obra/superpowers](https://github.com/obra/superpowers)

A battle-tested set of core disciplines and autonomous agent execution protocols designed to eliminate sloppy implementations, untested code, and shallow debugging.

---

## 🛠️ The 5 Core Superpowers

### 1. `systematic-debugging`
Never guess or apply blind patches. Follow the strict 4-phase debugging protocol:
1. **Reproduce**: Create a minimal reproducible test case that fails reliably.
2. **Isolate Root Cause**: Trace the exact variable, network failure, or logic error before writing fixes.
3. **Test-Driven Fix**: Write a test verifying the expected behavior, then implement the minimal necessary fix.
4. **Regression Check**: Run the full test suite to guarantee zero side effects.

### 2. `test-driven-development` (TDD)
- **Red**: Write a failing unit or integration test defining the contract before touching production code.
- **Green**: Implement the simplest code that makes the test pass.
- **Refactor**: Clean up the implementation while keeping all tests green.

### 3. `verification-before-completion`
- Never report a task as complete without verifiable evidence:
  - CLI command exit code `0`.
  - HTTP `200 OK` response payload.
  - Passing test suite output.
- Claims without proof are rejected by the system.

### 4. `defensive-architecture`
- Strict input validation at every API boundary using Pydantic / TypeScript Zod.
- Explicit error handling for network timeouts, schema drifts, and external API failures.
- No silent failures: log structured, timestamped telemetry for every operation.

### 5. `adversarial-code-review`
- Review every modified file against:
  - Security vulnerabilities (no hardcoded secrets, injection vectors, or ungrounded claims).
  - Performance bottlenecks (no unindexed database queries or infinite retry loops).
  - Type integrity (no unchecked `any` casts).
