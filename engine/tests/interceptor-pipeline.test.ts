import {
  IDEHookContext,
  AuditLedger,
  InMemoryStorage,
  DeterministicStateMachine,
  InterceptorRunner,
  PlanApprovalGuard,
  ScopeBoundaryGuard,
  CommandSafetyGuard,
  ASTLSPValidator,
  AntiTruncationGuard,
  ReviewFreezeGuard,
  PromptAssembler,
  FileWriteToolCall,
  CommandToolCall,
} from '../src/index.js';

// Zero-dependency test assertion utilities
function assertStrictEqual<T>(actual: T, expected: T, message?: string) {
  if (actual !== expected) {
    throw new Error(message || `Assertion Failed: expected '${expected}', got '${actual}'`);
  }
}

function assertTrue(value: boolean, message?: string) {
  if (!value) {
    throw new Error(message || 'Assertion Failed: value is not true');
  }
}

async function runTests() {
  console.log('🧪 Starting Antigravity IDE Engine Interceptor & Pipeline Tests (Zero-Dependency)...\n');

  const testWorkspace = 'C:/antigravity/test_workspace';
  const storage = new InMemoryStorage();

  const context: IDEHookContext = {
    sessionId: 'test-session-001',
    workspaceRoot: testWorkspace,
    currentPhase: 'Implement',
    modifiedFiles: new Set<string>(),
  };

  const ledger = new AuditLedger(testWorkspace, storage);
  const stateMachine = new DeterministicStateMachine(context, ledger);
  const runner = new InterceptorRunner(context, ledger);

  // Register Hooks
  runner.registerPreHook(new PlanApprovalGuard());
  runner.registerPreHook(new ScopeBoundaryGuard());
  runner.registerPreHook(new CommandSafetyGuard());
  runner.registerPostHook(new ASTLSPValidator());
  runner.registerPostHook(new AntiTruncationGuard());
  stateMachine.registerTransitionHook(new ReviewFreezeGuard());

  const mockExecutor = (call: { args: { TargetFile?: string; CommandLine?: string } }) => ({
    status: 'executed',
    target: call.args.TargetFile || call.args.CommandLine,
  });

  // Test 1: Plan Approval Guard - Unapproved Plan Mutation
  console.log('▶ Test 1: PlanApprovalGuard blocks mutation before plan approval');
  const unapprovedCall: FileWriteToolCall = {
    toolName: 'write_to_file',
    args: {
      TargetFile: `${testWorkspace}/src/app.ts`,
      CodeContent: 'console.log("hello");',
    },
  };
  const res1 = await runner.dispatchToolCall(unapprovedCall, mockExecutor);
  assertStrictEqual(res1.hookResult.decision, 'BLOCK');
  if (res1.hookResult.decision === 'BLOCK') {
    assertStrictEqual(res1.hookResult.code, 'PLAN_APPROVAL_REQUIRED');
  }
  console.log('  ✅ Blocked correctly: PLAN_APPROVAL_REQUIRED\n');

  // Test 2: Approve Plan and Allow in-scope mutation
  console.log('▶ Test 2: User explicitly approves plan -> in-scope mutation allowed');
  const planContent = '# Implementation Plan\n\n## Proposed Changes\n- src/app.ts\n- src/utils.ts';
  stateMachine.approvePlan('implementation_plan.md', planContent, ['src/app.ts', 'src/utils.ts']);

  const approvedCall: FileWriteToolCall = {
    toolName: 'write_to_file',
    args: {
      TargetFile: `${testWorkspace}/src/app.ts`,
      CodeContent: 'export const run = () => console.log("running");',
    },
  };
  const res2 = await runner.dispatchToolCall(approvedCall, mockExecutor);
  assertStrictEqual(res2.hookResult.decision, 'ALLOW');
  console.log('  ✅ Allowed in-scope mutation successfully\n');

  // Test 3: Scope Boundary Guard - Out of Scope file
  console.log('▶ Test 3: ScopeBoundaryGuard blocks out-of-scope mutation');
  const outOfScopeCall: FileWriteToolCall = {
    toolName: 'write_to_file',
    args: {
      TargetFile: `${testWorkspace}/src/secret.ts`,
      CodeContent: 'export const secret = 123;',
    },
  };
  const res3 = await runner.dispatchToolCall(outOfScopeCall, mockExecutor);
  assertStrictEqual(res3.hookResult.decision, 'BLOCK');
  if (res3.hookResult.decision === 'BLOCK') {
    assertStrictEqual(res3.hookResult.code, 'OUT_OF_SCOPE_MUTATION');
  }
  console.log('  ✅ Blocked correctly: OUT_OF_SCOPE_MUTATION\n');

  // Test 4: Command Safety Guard - Destructive command blocked
  console.log('▶ Test 4: CommandSafetyGuard blocks destructive shell command');
  const dangerousCmd: CommandToolCall = {
    toolName: 'run_command',
    args: {
      CommandLine: 'rm -rf /',
      Cwd: testWorkspace,
    },
  };
  const res4 = await runner.dispatchToolCall(dangerousCmd, mockExecutor);
  assertStrictEqual(res4.hookResult.decision, 'BLOCK');
  if (res4.hookResult.decision === 'BLOCK') {
    assertStrictEqual(res4.hookResult.code, 'DESTRUCTIVE_COMMAND_DENIED');
  }
  console.log('  ✅ Blocked correctly: DESTRUCTIVE_COMMAND_DENIED\n');

  // Test 5: Anti-Truncation Guard - Block lazy placeholder comments
  console.log('▶ Test 5: AntiTruncationGuard blocks lazy comments (// ... rest of the code ...)');
  const lazyCall: FileWriteToolCall = {
    toolName: 'write_to_file',
    args: {
      TargetFile: `${testWorkspace}/src/app.ts`,
      CodeContent: 'function test() {\n  // ... rest of the code ...\n}',
    },
  };
  const res5 = await runner.dispatchToolCall(lazyCall, mockExecutor);
  assertStrictEqual(res5.hookResult.decision, 'BLOCK');
  if (res5.hookResult.decision === 'BLOCK') {
    assertStrictEqual(res5.hookResult.code, 'LAZY_TRUNCATION_DETECTED');
  }
  console.log('  ✅ Blocked correctly: LAZY_TRUNCATION_DETECTED\n');

  // Test 6: AST / LSP Validator - Block malformed JSON
  console.log('▶ Test 6: ASTLSPValidator blocks malformed JSON syntax');
  const malformedJsonCall: FileWriteToolCall = {
    toolName: 'write_to_file',
    args: {
      TargetFile: `${testWorkspace}/config.json`,
      CodeContent: '{ "name": "app", invalid_json }',
    },
  };
  const res6 = await runner.dispatchToolCall(malformedJsonCall, mockExecutor);
  assertStrictEqual(res6.hookResult.decision, 'BLOCK');
  if (res6.hookResult.decision === 'BLOCK') {
    assertStrictEqual(res6.hookResult.code, 'JSON_SYNTAX_ERROR');
  }
  console.log('  ✅ Blocked correctly: JSON_SYNTAX_ERROR\n');

  // Test 7: Review Freeze Guard - Block unverified transition to Verify
  console.log('▶ Test 7: ReviewFreezeGuard blocks transition without test pass evidence');
  const transitionRes = await stateMachine.transitionTo('Verify');
  assertStrictEqual(transitionRes.decision, 'BLOCK');
  if (transitionRes.decision === 'BLOCK') {
    assertStrictEqual(transitionRes.code, 'UNVERIFIED_COMPLETION_ATTEMPT');
  }
  console.log('  ✅ Blocked correctly: UNVERIFIED_COMPLETION_ATTEMPT\n');

  // Test 8: Record test evidence and allow transition
  console.log('▶ Test 8: Record test pass evidence -> phase transition allowed');
  context.recentTestPassHash = 'mock-sha256-test-pass';
  const validTransition = await stateMachine.transitionTo('Verify');
  assertStrictEqual(validTransition.decision, 'ALLOW');
  assertStrictEqual(context.currentPhase, 'Verify');
  console.log('  ✅ Allowed transition to Verify\n');

  // Test 9: Audit Ledger Verification
  console.log('▶ Test 9: Verify immutable audit events in ledger');
  const events = ledger.getEvents();
  assertTrue(events.length >= 6, `Expected at least 6 events, got ${events.length}`);
  console.log(`  ✅ Successfully recorded ${events.length} audit trail events in JSONL\n`);

  // Test 10: Prompt Assembler Verification
  console.log('▶ Test 10: Verify PromptAssembler Tiered Structure');
  const prompt = PromptAssembler.assemblePrompt(context, 'Custom Project Rule: Use PascalCase for classes.');
  assertTrue(prompt.includes('Antigravity IDE Core Invariants'));
  assertTrue(prompt.includes('Current Phase: Verify'));
  assertTrue(prompt.includes('Custom Project Rule: Use PascalCase'));
  console.log('  ✅ Prompt synthesized accurately with all invariants and rules\n');

  console.log('🎉 ALL 10 INTERCEPTOR & PIPELINE TESTS PASSED PERFECTLY!\n');
}

runTests().catch(err => {
  console.error('❌ Test failed:', err);
});
