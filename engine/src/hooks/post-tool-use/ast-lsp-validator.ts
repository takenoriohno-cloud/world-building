import { PostToolUseHook, ToolCall, IDEHookContext, HookResult, FileWriteToolCall } from '../../types/index.js';

export class ASTLSPValidator implements PostToolUseHook {
  public name = 'ast-lsp-validator';

  public execute(call: ToolCall, _context: IDEHookContext): HookResult {
    if (!['write_to_file', 'replace_file_content', 'multi_replace_file_content'].includes(call.toolName)) {
      return { decision: 'ALLOW' };
    }

    const fileCall = call as FileWriteToolCall;
    const content = fileCall.args.CodeContent || fileCall.args.ReplacementContent || '';
    const targetFile = fileCall.args.TargetFile;

    // Fast AST / Syntax heuristics
    if (targetFile.endsWith('.json')) {
      try {
        if (content.trim().length > 0) {
          JSON.parse(content);
        }
      } catch (err: unknown) {
        const errorMsg = err instanceof Error ? err.message : String(err);
        return {
          decision: 'BLOCK',
          code: 'JSON_SYNTAX_ERROR',
          reason: `JSON parsing failed for '${targetFile}': ${errorMsg}`,
          recoveryPrompt: `[BLOCK 422: JSON Syntax Error Detected]
The JSON content written to '${targetFile}' contains syntax errors:
${errorMsg}

Please fix the formatting (e.g. missing commas, unescaped quotes) and re-output the valid JSON.`,
        };
      }
    }

    // Basic Bracket / Parenthesis balance validator for JS/TS
    if (targetFile.endsWith('.ts') || targetFile.endsWith('.js') || targetFile.endsWith('.tsx')) {
      const openBraces = (content.match(/\{/g) || []).length;
      const closeBraces = (content.match(/\}/g) || []).length;
      if (openBraces !== closeBraces && call.toolName === 'write_to_file') {
        return {
          decision: 'BLOCK',
          code: 'UNBALANCED_BRACES_DETECTED',
          reason: `Unbalanced braces in '${targetFile}': ${openBraces} open vs ${closeBraces} close.`,
          recoveryPrompt: `[BLOCK 422: Syntax Error - Unbalanced Braces]
Your output for '${targetFile}' has unbalanced curly braces ({: ${openBraces}, }: ${closeBraces}).
This will cause syntax errors. Please provide the complete, properly closed file content.`,
        };
      }
    }

    return { decision: 'ALLOW' };
  }
}
