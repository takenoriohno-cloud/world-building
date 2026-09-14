import { PathUtils } from '../../utils/path-utils.js';
import { PreToolUseHook, ToolCall, IDEHookContext, HookResult, FileWriteToolCall } from '../../types/index.js';

export class PlanApprovalGuard implements PreToolUseHook {
  public name = 'plan-approval-guard';

  public execute(call: ToolCall, context: IDEHookContext): HookResult {
    // Check if tool is modifying filesystem
    if (!['write_to_file', 'replace_file_content', 'multi_replace_file_content'].includes(call.toolName)) {
      return { decision: 'ALLOW' };
    }

    const fileCall = call as FileWriteToolCall;
    const targetFile = fileCall.args.TargetFile;

    // Allow editing plan, spec, or audit files without prior plan approval
    const normalized = PathUtils.normalize(targetFile);
    if (
      normalized.includes('/.specify/plans/') ||
      normalized.includes('/.specify/specs/') ||
      normalized.includes('/.specify/tasks/') ||
      normalized.includes('/doc/') ||
      normalized.endsWith('implementation_plan.md') ||
      normalized.endsWith('.log')
    ) {
      return { decision: 'ALLOW' };
    }

    // If attempting to write source/content files without an approved plan
    if (!context.activePlan || !context.activePlan.planHash) {
      return {
        decision: 'BLOCK',
        code: 'PLAN_APPROVAL_REQUIRED',
        reason: `Cannot modify implementation file '${PathUtils.basename(targetFile)}' without an approved plan.`,
        recoveryPrompt: `[BLOCK 403: Plan Approval Required]
You are attempting to modify source files before the user has approved the implementation plan.
Target File: ${targetFile}

Required Actions:
1. Conduct read-only codebase research if needed.
2. Create or update '.specify/plans/*.plan.md' or the 'implementation_plan.md' artifact.
3. HALT and request explicit user approval before writing code.`,
      };
    }

    return { decision: 'ALLOW' };
  }
}
