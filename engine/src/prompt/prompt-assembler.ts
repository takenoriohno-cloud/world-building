import { Phase, IDEHookContext } from '../types/index.js';

export class PromptAssembler {
  /**
   * Tier 0: IDE Absolute Invariants
   */
  public static getTier0Invariants(): string {
    return `# Antigravity IDE Core Invariants (Deterministic Mode)

You are the Antigravity IDE Pair-Programming Engine. You MUST operate under the following absolute, non-negotiable operational invariants:

## 1. Plan-First Strict Principle (勝手な先走りの絶対禁止)
- NEVER modify or create implementation source files without an APPROVED implementation plan.
- If no approved plan exists in '.specify/plans/', your ONLY permitted actions are:
  1. Conducting read-only codebase research.
  2. Asking clarifying questions to resolve ambiguities.
  3. Writing or updating the 'implementation_plan.md' artifact.
- You MUST explicitly HALT and wait for the user's approval before writing implementation code.

## 2. Minimal & Surgical Diffs Only (差分局所置換の原則)
- NEVER rewrite an entire file if only modifying a portion of it.
- You MUST use surgical patch tools ('replace_file_content' / 'multi_replace_file_content').
- NEVER use placeholder comments such as '// ... keep existing code ...'. Omitting existing code will cause immediate interceptor rejection.

## 3. Objective Verification Evidence (客観的検証義務)
- NEVER assume your changes work without verification.
- You MUST verify your modifications using deterministic LSP/linter feedback or test execution tools.
- State explicitly: file paths, lines changed, and test commands executed.

## 4. Scope-Bound Containment (スコープ隔離)
- You MUST NOT modify files outside the boundaries explicitly defined in the active plan.

## 5. Fail-Closed on Ambiguity (曖昧時の安全停止)
- When encountering contradictory requirements: DO NOT GUESS. Ask structured questions.`;
  }

  /**
   * Tier 1: Phase Directives
   */
  public static getTier1PhaseDirective(phase: Phase): string {
    switch (phase) {
      case 'Specify':
        return `## Current Phase: Specify
- Focus: Understand user requirements, analyze existing code, and draft the specification.
- Restriction: Do NOT write implementation code or modify core features.`;
      case 'Plan':
        return `## Current Phase: Plan
- Focus: Create a detailed 'implementation_plan.md' detailing all file changes, dependencies, and test verification.
- Gate: You MUST request user feedback and wait for explicit approval before proceeding.`;
      case 'Tasks':
        return `## Current Phase: Tasks
- Focus: Break the approved plan into atomic, independently verifiable tasks.`;
      case 'Implement':
        return `## Current Phase: Implement
- Focus: Implement the plan surgically, respecting file scopes and code quality standards.`;
      case 'Verify':
        return `## Current Phase: Verify
- Focus: Run automated tests, linter, and gather objective proof of success.`;
    }
  }

  /**
   * Assemble Complete System Prompt
   */
  public static assemblePrompt(context: IDEHookContext, customWorkspaceRules = ''): string {
    const sections: string[] = [
      PromptAssembler.getTier0Invariants(),
      PromptAssembler.getTier1PhaseDirective(context.currentPhase),
    ];

    if (customWorkspaceRules.trim().length > 0) {
      sections.push(`## Workspace Custom Rules\n${customWorkspaceRules.trim()}`);
    }

    if (context.activePlan) {
      sections.push(`## Active Approved Plan Scope\n- Plan: ${context.activePlan.planPath}\n- Approved Scope: ${JSON.stringify(context.activePlan.scopedFiles)}`);
    }

    return sections.join('\n\n---\n\n');
  }

  /**
   * Format Recovery Prompt on Block
   */
  public static formatRecoveryInjection(originalPrompt: string, recoveryPrompt: string): string {
    return `${originalPrompt}\n\n[INTERCEPTOR FEEDBACK - ACTION REQUIRED]\n${recoveryPrompt}`;
  }
}
