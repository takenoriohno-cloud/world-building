import { PreTransitionHook, Phase, IDEHookContext, HookResult } from '../../types/index.js';

export class ReviewFreezeGuard implements PreTransitionHook {
  public name = 'review-freeze-guard';

  public execute(fromPhase: Phase, toPhase: Phase, context: IDEHookContext): HookResult {
    // When transitioning from Implement to Verify or completing tasks
    if (fromPhase === 'Implement' && toPhase === 'Verify') {
      if (context.modifiedFiles.size > 0 && !context.recentTestPassHash) {
        return {
          decision: 'BLOCK',
          code: 'UNVERIFIED_COMPLETION_ATTEMPT',
          reason: `Files were modified during implementation without running automated verification.`,
          recoveryPrompt: `[BLOCK 412: Unverified Completion Attempt]
You modified ${context.modifiedFiles.size} file(s) during the Implementation phase, but have not executed automated tests or static analysis.

Modified Files: ${Array.from(context.modifiedFiles).join(', ')}

Required Actions:
1. Run automated tests (e.g. 'npm test', 'tsc --noEmit', or targeted test scripts).
2. Confirm that tests exit with code 0.
3. Record the verification result before declaring completion.`,
        };
      }
    }

    return { decision: 'ALLOW' };
  }
}
