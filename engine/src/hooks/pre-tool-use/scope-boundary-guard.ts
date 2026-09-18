import { PathUtils } from '../../utils/path-utils.js';
import { PreToolUseHook, ToolCall, IDEHookContext, HookResult, FileWriteToolCall } from '../../types/index.js';

export class ScopeBoundaryGuard implements PreToolUseHook {
  public name = 'scope-boundary-guard';

  public execute(call: ToolCall, context: IDEHookContext): HookResult {
    if (!['write_to_file', 'replace_file_content', 'multi_replace_file_content'].includes(call.toolName)) {
      return { decision: 'ALLOW' };
    }

    const fileCall = call as FileWriteToolCall;
    const targetFile = PathUtils.normalize(fileCall.args.TargetFile);
    const workspaceRoot = PathUtils.normalize(context.workspaceRoot);

    // 1. Path Traversal Check (Must be within workspace)
    if (!targetFile.startsWith(workspaceRoot) && !targetFile.includes('.gemini')) {
      return {
        decision: 'BLOCK',
        code: 'PATH_TRAVERSAL_DETECTED',
        reason: `Target file '${targetFile}' is outside workspace root '${workspaceRoot}'.`,
        recoveryPrompt: `[BLOCK 403: Workspace Boundary Violation]
The file '${targetFile}' is located outside the active workspace.
All modifications must stay strictly inside '${workspaceRoot}'.`,
      };
    }

    // 2. Plan Scope Check (If active plan is present)
    if (context.activePlan && context.activePlan.scopedFiles && context.activePlan.scopedFiles.length > 0) {
      const isAllowed = context.activePlan.scopedFiles.some((allowedPattern: string) => {
        const normalizedAllowed = PathUtils.normalize(allowedPattern);
        return targetFile.endsWith(normalizedAllowed) || targetFile.includes('/' + normalizedAllowed);
      });

      // Also allow artifacts/docs/plans
      const isDocOrArtifact = 
        targetFile.includes('/.specify/') ||
        targetFile.includes('/doc/') ||
        targetFile.includes('.gemini') ||
        targetFile.endsWith('.plan.md');

      if (!isAllowed && !isDocOrArtifact) {
        return {
          decision: 'BLOCK',
          code: 'OUT_OF_SCOPE_MUTATION',
          reason: `File '${PathUtils.basename(targetFile)}' is not listed in the approved plan scope.`,
          recoveryPrompt: `[BLOCK 403: Scope Boundary Violation]
The file '${targetFile}' is not included in the approved plan's scope:
Approved Scoped Files: ${JSON.stringify(context.activePlan.scopedFiles)}

If this change is necessary:
1. STOP file editing.
2. Update the implementation plan to include this file.
3. Request user re-approval for the expanded scope.`,
        };
      }
    }

    return { decision: 'ALLOW' };
  }
}
