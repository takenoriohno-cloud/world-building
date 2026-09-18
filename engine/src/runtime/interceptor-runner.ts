import {
  IDEHookContext,
  ToolCall,
  HookResult,
  PreToolUseHook,
  PostToolUseHook,
  FileWriteToolCall,
} from '../types/index.js';
import { AuditLedger } from '../state/audit-ledger.js';

export class InterceptorRunner {
  private preHooks: PreToolUseHook[] = [];
  private postHooks: PostToolUseHook[] = [];
  private context: IDEHookContext;
  private ledger: AuditLedger;

  constructor(context: IDEHookContext, ledger: AuditLedger) {
    this.context = context;
    this.ledger = ledger;
  }

  public registerPreHook(hook: PreToolUseHook): void {
    this.preHooks.push(hook);
  }

  public registerPostHook(hook: PostToolUseHook): void {
    this.postHooks.push(hook);
  }

  /**
   * Intercept and run a tool call through the deterministic envelope
   */
  public async dispatchToolCall(
    call: ToolCall,
    executor: (call: ToolCall) => Promise<unknown> | unknown
  ): Promise<{ result?: unknown; hookResult: HookResult }> {
    // 1. Pre-Tool-Use Interception
    for (const hook of this.preHooks) {
      const preRes = await hook.execute(call, this.context);
      if (preRes.decision === 'BLOCK') {
        this.ledger.recordEvent({
          sessionId: this.context.sessionId,
          phase: this.context.currentPhase,
          eventType: 'TOOL_BLOCKED',
          details: { stage: 'PreToolUse', hook: hook.name, call, reason: preRes.reason },
        });
        return { hookResult: preRes };
      }
    }

    // 2. Execute Tool (e.g. disk write or command)
    let output: unknown;
    try {
      output = await executor(call);
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      return {
        hookResult: {
          decision: 'BLOCK',
          code: 'TOOL_EXECUTION_ERROR',
          reason: `Tool '${call.toolName}' threw an error: ${errorMsg}`,
          recoveryPrompt: `[TOOL ERROR] Tool execution failed: ${errorMsg}`,
        },
      };
    }

    // Track modified file
    if (['write_to_file', 'replace_file_content', 'multi_replace_file_content'].includes(call.toolName)) {
      const fileCall = call as FileWriteToolCall;
      this.context.modifiedFiles.add(fileCall.args.TargetFile);
    }

    // 3. Post-Tool-Use Interception
    for (const hook of this.postHooks) {
      const postRes = await hook.execute(call, this.context, output);
      if (postRes.decision === 'BLOCK') {
        this.ledger.recordEvent({
          sessionId: this.context.sessionId,
          phase: this.context.currentPhase,
          eventType: 'TOOL_BLOCKED',
          details: { stage: 'PostToolUse', hook: hook.name, call, reason: postRes.reason },
        });
        return { result: output, hookResult: postRes };
      }
    }

    // 4. Log Success in Immutable Ledger
    this.ledger.recordEvent({
      sessionId: this.context.sessionId,
      phase: this.context.currentPhase,
      eventType: 'TOOL_ALLOWED',
      details: { call },
    });

    return { result: output, hookResult: { decision: 'ALLOW' } };
  }
}
