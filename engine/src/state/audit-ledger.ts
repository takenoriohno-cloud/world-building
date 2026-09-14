import { PathUtils } from '../utils/path-utils.js';
import { AuditEvent } from '../types/index.js';

export interface LedgerStorage {
  append(filePath: string, line: string): void;
  read(filePath: string): string;
  exists(filePath: string): boolean;
}

// In-Memory fallback storage for environments without Node.js fs
export class InMemoryStorage implements LedgerStorage {
  private store: Map<string, string> = new Map();

  public append(filePath: string, line: string): void {
    const current = this.store.get(filePath) || '';
    this.store.set(filePath, current + line);
  }

  public read(filePath: string): string {
    return this.store.get(filePath) || '';
  }

  public exists(filePath: string): boolean {
    return this.store.has(filePath);
  }
}

export class AuditLedger {
  private ledgerPath: string;
  private storage: LedgerStorage;

  constructor(workspaceRoot: string, storage?: LedgerStorage) {
    const normalizedRoot = PathUtils.normalize(workspaceRoot);
    this.ledgerPath = `${normalizedRoot}/.specify/audit/audit.jsonl`;
    this.storage = storage || new InMemoryStorage();
  }

  public recordEvent(event: Omit<AuditEvent, 'timestamp'>): AuditEvent {
    const fullEvent: AuditEvent = {
      timestamp: new Date().toISOString(),
      ...event,
    };

    const line = JSON.stringify(fullEvent) + '\n';
    this.storage.append(this.ledgerPath, line);
    return fullEvent;
  }

  public getEvents(): AuditEvent[] {
    if (!this.storage.exists(this.ledgerPath)) {
      return [];
    }
    const content = this.storage.read(this.ledgerPath).trim();
    if (content.length === 0) {
      return [];
    }
    const lines = content.split('\n');
    return lines
      .filter((line: string) => line.trim().length > 0)
      .map((line: string) => JSON.parse(line) as AuditEvent);
  }

  /**
   * Fast, zero-dependency deterministic string hashing (DJB2/FNV-1a variant)
   */
  public computePlanHash(planContent: string): string {
    let hash = 0x811c9dc5;
    const str = planContent.trim();
    for (let i = 0; i < str.length; i++) {
      hash ^= str.charCodeAt(i);
      hash = (hash * 0x01000193) >>> 0;
    }
    return hash.toString(16).padStart(8, '0');
  }
}
