import { IDEHookContext, Phase, PlanEvidence, PreTransitionHook, HookResult } from '../types/index.js';
import { AuditLedger } from './audit-ledger.js';

export class DeterministicStateMachine {
  private context: IDEHookContext;
  private ledger: AuditLedger;
  private preTransitionHooks: PreTransitionHook[] = [];

  constructor(context: IDEHookContext, ledger: AuditLedger) {
    this.context = context;
    this.ledger = ledger;
  }

  public registerTransitionHook(hook: PreTransitionHook): void {
    this.preTransitionHooks.push(hook);
  }

  public getContext(): Readonly<IDEHookContext> {
    return this.context;
  }

  public approvePlan(planPath: string, planContent: string, scopedFiles: string[]): PlanEvidence {
    const hash = this.ledger.computePlanHash(planContent);
    const evidence: PlanEvidence = {
      planPath,
      planHash: hash,
      approvedBy: 'USER_EXPLICIT',
      approvedAt: new Date().toISOString(),
      scopedFiles,
    };

    this.context.activePlan = evidence;
    this.ledger.recordEvent({
      sessionId: this.context.sessionId,
      phase: this.context.currentPhase,
      eventType: 'PLAN_APPROVED',
      details: { planPath, planHash: hash, scopedFiles },
    });

    return evidence;
  }

  public async transitionTo(targetPhase: Phase): Promise<HookResult> {
    const current = this.context.currentPhase;

    // Validate valid lifecycle transitions
    const validTransitions: Record<Phase, Phase[]> = {
      Specify: ['Plan'],
      Plan: ['Tasks', 'Implement'],
      Tasks: ['Implement'],
      Implement: ['Verify', 'Plan'],
      Verify: ['Implement', 'Specify'],
    };

    if (!validTransitions[current]?.includes(targetPhase)) {
      return {
        decision: 'BLOCK',
        code: 'INVALID_TRANSITION',
        reason: `Cannot transition directly from phase '${current}' to '${targetPhase}'.`,
        recoveryPrompt: `[BLOCK 400: Invalid Phase Transition] Permitted transitions from '${current}' are: ${validTransitions[current]?.join(', ')}.`,
      };
    }

    // Run PreTransition Hooks
    for (const hook of this.preTransitionHooks) {
      const res = await hook.execute(current, targetPhase, this.context);
      if (res.decision === 'BLOCK') {
        this.ledger.recordEvent({
          sessionId: this.context.sessionId,
          phase: current,
          eventType: 'TOOL_BLOCKED',
          details: { hook: hook.name, targetPhase, reason: res.reason },
        });
        return res;
      }
    }

    // Transition successfully
    this.context.currentPhase = targetPhase;
    this.ledger.recordEvent({
      sessionId: this.context.sessionId,
      phase: targetPhase,
      eventType: 'PHASE_TRANSITION',
      details: { from: current, to: targetPhase },
    });

    return { decision: 'ALLOW', reason: `Transitioned from ${current} to ${targetPhase}` };
  }
}
