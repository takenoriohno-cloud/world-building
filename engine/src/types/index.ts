/**
 * Antigravity IDE - Core Types & Interceptor Definitions
 */

export type Phase = 'Specify' | 'Plan' | 'Tasks' | 'Implement' | 'Verify';

export interface PlanEvidence {
  planPath: string;
  planHash: string;
  approvedBy: 'USER_EXPLICIT' | 'TEST_HARNESS';
  approvedAt: string;
  scopedFiles: string[];
}

export interface IDEHookContext {
  sessionId: string;
  workspaceRoot: string;
  currentPhase: Phase;
  activeSpecPath?: string;
  activePlan?: PlanEvidence;
  recentTestPassHash?: string;
  modifiedFiles: Set<string>;
}

export interface BaseToolCall {
  toolName: string;
  args: Record<string, unknown>;
}

export interface FileWriteToolCall extends BaseToolCall {
  toolName: 'write_to_file' | 'replace_file_content' | 'multi_replace_file_content';
  args: {
    TargetFile: string;
    CodeContent?: string;
    ReplacementContent?: string;
    TargetContent?: string;
    Instruction?: string;
    Overwrite?: boolean;
  };
}

export interface CommandToolCall extends BaseToolCall {
  toolName: 'run_command';
  args: {
    CommandLine: string;
    Cwd: string;
    WaitMsBeforeAsync?: number;
    IsDaemon?: boolean;
  };
}

export type ToolCall = FileWriteToolCall | CommandToolCall | BaseToolCall;

export type HookDecision = 'ALLOW' | 'BLOCK';

export interface AllowResult {
  decision: 'ALLOW';
  reason?: string;
}

export interface BlockResult {
  decision: 'BLOCK';
  code: string;
  reason: string;
  recoveryPrompt: string;
}

export type HookResult = AllowResult | BlockResult;

export interface PreToolUseHook {
  name: string;
  execute(call: ToolCall, context: IDEHookContext): Promise<HookResult> | HookResult;
}

export interface PostToolUseHook {
  name: string;
  execute(call: ToolCall, context: IDEHookContext, toolOutput?: unknown): Promise<HookResult> | HookResult;
}

export interface PreTransitionHook {
  name: string;
  execute(fromPhase: Phase, toPhase: Phase, context: IDEHookContext): Promise<HookResult> | HookResult;
}

export interface AuditEvent {
  timestamp: string;
  sessionId: string;
  phase: Phase;
  eventType: 'TOOL_INTERCEPTED' | 'TOOL_ALLOWED' | 'TOOL_BLOCKED' | 'PHASE_TRANSITION' | 'PLAN_APPROVED';
  details: Record<string, unknown>;
}

export interface ASTDiagnostic {
  file: string;
  line: number;
  column: number;
  severity: 'error' | 'warning';
  message: string;
  code?: string;
}
