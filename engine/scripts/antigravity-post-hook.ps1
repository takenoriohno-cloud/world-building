# Antigravity IDE PostToolUse Hook Adapter (Deterministic Validator & Audit Ledger)
# Receives JSON from stdin, outputs result JSON to stdout

[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$inputJson = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($inputJson)) {
    @{ decision = "allow" } | ConvertTo-Json -Compress
    exit 0
}

try {
    $payload = $inputJson | ConvertFrom-Json
} catch {
    @{ decision = "allow" } | ConvertTo-Json -Compress
    exit 0
}

$toolName = $payload.toolCall.name
$args = $payload.toolCall.args
$workspaceRoot = if ($payload.workspacePaths -and $payload.workspacePaths.Count -gt 0) { $payload.workspacePaths[0] } else { "." }

# --- POST-TOOL VALIDATORS ---

if ($toolName -in @("write_to_file", "replace_file_content", "multi_replace_file_content")) {
    $content = if ($args.CodeContent) { $args.CodeContent } else { $args.ReplacementContent }
    $targetFile = $args.TargetFile

    # 1. Anti-Truncation Guard
    if ($content -match "\/\/\s*\.{3,}\s*(rest of the code|keep unchanged|same as before|existing code)" -or
        $content -match "\/\*\s*\.{3,}\s*(rest of code|unchanged)\s*\.{0,3}\s*\*\/" -or
        $content -match "\/\/\s*TODO:\s*(implement remaining|keep existing)") {
        
        $response = @{
            decision = "deny"
            reason = "[BLOCK 422: Lazy Truncation Detected] Omitting code with placeholder comments is forbidden in '$targetFile'. Please output full, un-truncated content."
        }
        $response | ConvertTo-Json -Compress
        exit 0
    }

    # 2. JSON Syntax Validator
    if ($targetFile -and $targetFile.EndsWith(".json")) {
        try {
            if (-not [string]::IsNullOrWhiteSpace($content)) {
                $null = $content | ConvertFrom-Json
            }
        } catch {
            $response = @{
                decision = "deny"
                reason = "[BLOCK 422: JSON Syntax Error] Malformed JSON detected in '$targetFile'. Please fix formatting syntax."
            }
            $response | ConvertTo-Json -Compress
            exit 0
        }
    }
}

# --- AUDIT LEDGER RECORDING ---
try {
    $auditDir = Join-Path $workspaceRoot ".specify/audit"
    if (-not (Test-Path $auditDir)) {
        New-Item -ItemType Directory -Path $auditDir -Force | Out-Null
    }
    $ledgerPath = Join-Path $auditDir "audit.jsonl"
    $entry = @{
        timestamp = (Get-Date).ToString("o")
        conversationId = $payload.conversationId
        toolName = $toolName
        eventType = "TOOL_EXECUTED"
        target = if ($args.TargetFile) { $args.TargetFile } else { $args.CommandLine }
    } | ConvertTo-Json -Compress
    Add-Content -Path $ledgerPath -Value $entry
} catch {
    # Logging failure must not block execution
}

@{ decision = "allow" } | ConvertTo-Json -Compress
exit 0
