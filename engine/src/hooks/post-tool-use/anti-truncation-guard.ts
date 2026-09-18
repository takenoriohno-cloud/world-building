import { PostToolUseHook, ToolCall, IDEHookContext, HookResult, FileWriteToolCall } from '../../types/index.js';

export class AntiTruncationGuard implements PostToolUseHook {
  public name = 'anti-truncation-guard';

  private lazyPatterns: RegExp[] = [
    /\/\/\s*\.{3,}\s*(rest of the code|keep unchanged|same as before|existing code)\s*\.{0,3}/i,
    /\/\*\s*\.{3,}\s*(rest of code|unchanged)\s*\.{0,3}\s*\*\//i,
    /#\s*\.{3,}\s*(rest of code|keep existing)/i,
    /\/\/\s*TODO:\s*(implement remaining|keep existing)/i,
  ];

  public execute(call: ToolCall, _context: IDEHookContext): HookResult {
    if (!['write_to_file', 'replace_file_content', 'multi_replace_file_content'].includes(call.toolName)) {
      return { decision: 'ALLOW' };
    }

    const fileCall = call as FileWriteToolCall;
    const content = fileCall.args.CodeContent || fileCall.args.ReplacementContent || '';
    const targetFile = fileCall.args.TargetFile;

    // Check for lazy truncation patterns
    for (const pattern of this.lazyPatterns) {
      if (pattern.test(content)) {
        return {
          decision: 'BLOCK',
          code: 'LAZY_TRUNCATION_DETECTED',
          reason: `Code truncation placeholder matching '${pattern}' found in '${targetFile}'.`,
          recoveryPrompt: `[BLOCK 422: Lazy Code Truncation Detected]
You included a placeholder comment indicating omitted code (e.g. "// ... rest of code ...").
In Antigravity IDE, replacing working code with placeholders is strictly forbidden.

Required Action:
- If modifying a portion of a file, use 'replace_file_content' with precise, surgical TargetContent.
- If overwriting the whole file, supply the complete, un-truncated code.`,
        };
      }
    }

    return { decision: 'ALLOW' };
  }
}
