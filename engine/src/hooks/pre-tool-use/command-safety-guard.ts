import { PreToolUseHook, ToolCall, IDEHookContext, HookResult, CommandToolCall } from '../../types/index.js';

export class CommandSafetyGuard implements PreToolUseHook {
  public name = 'command-safety-guard';

  private dangerousPatterns: RegExp[] = [
    /\brm\s+-[rf]{1,2}\s+[\/\\]/i,         // rm -rf /
    /\bdel\s+\/s\s+\/q\s+[c-z]:\\/i,       // del /s /q C:\
    /\bgit\s+reset\s+--hard\b/i,            // git reset --hard
    /\bgit\s+clean\s+-[fdx]{1,3}\b/i,       // git clean -fdx
    /\bdrop\s+database\b/i,                 // DROP DATABASE
    /\bformat\s+[c-z]:/i,                   // format c:
    /\bmkfs\b/i,                            // mkfs
    /\b:(){ :\|:& };:/,                     // fork bomb
  ];

  public execute(call: ToolCall, _context: IDEHookContext): HookResult {
    if (call.toolName !== 'run_command') {
      return { decision: 'ALLOW' };
    }

    const cmdCall = call as CommandToolCall;
    const command = cmdCall.args.CommandLine;

    for (const pattern of this.dangerousPatterns) {
      if (pattern.test(command)) {
        return {
          decision: 'BLOCK',
          code: 'DESTRUCTIVE_COMMAND_DENIED',
          reason: `Execution of destructive command matching pattern '${pattern}' is blocked.`,
          recoveryPrompt: `[BLOCK 400: Destructive Command Intercepted]
The command you attempted to run was blocked for safety:
Command: '${command}'

Reason: Destructive or irreversible filesystem operations are prohibited in autonomous mode.
Please choose a non-destructive alternative or ask the user to run it manually.`,
        };
      }
    }

    return { decision: 'ALLOW' };
  }
}
