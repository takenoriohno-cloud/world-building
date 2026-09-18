# Antigravity IDE PreToolUse Hook Adapter (Deterministic Guard)
# Receives JSON from stdin, outputs decision JSON to stdout

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

# --- PRE-TOOL GUARDS ---

# 1. Plan Approval & Scope Boundary Guard (for file mutations)
if ($toolName -in @("write_to_file", "replace_file_content", "multi_replace_file_content")) {
    $targetFile = $args.TargetFile
    $normTarget = $targetFile.Replace("\", "/")

    # Exemption: Allow editing specs, plans, tasks, doc, audit, artifacts without prior plan
    $isExempt = $normTarget -like "*/.specify/*" -or 
                $normTarget -like "*/doc/*" -or 
                $normTarget -like "*/engine/*" -or 
                $normTarget -like "*implementation_plan.md" -or 
                $normTarget -like "*walkthrough.md" -or
                $normTarget -like "*.log"

    if (-not $isExempt) {
        # Check if an approved plan exists in .specify/plans
        $plansDir = Join-Path $workspaceRoot ".specify/plans"
        $hasApprovedPlan = $false

        if (Test-Path $plansDir) {
            $planFiles = Get-ChildItem -Path $plansDir -Filter "*.plan.md" -Recurse -ErrorAction SilentlyContinue
            if ($planFiles -and $planFiles.Count -gt 0) {
                $hasApprovedPlan = $true
            }
        }

        if (-not $hasApprovedPlan) {
            $response = @{
                decision = "deny"
                reason = "[BLOCK 403: Plan Approval Required] Cannot modify implementation source files without an approved plan in .specify/plans/. Please draft and approve the implementation plan first."
            }
            $response | ConvertTo-Json -Compress
            exit 0
        }
    }
}

# 2. Command Safety Guard (Destructive commands)
if ($toolName -eq "run_command") {
    $cmd = $args.CommandLine
    if ($cmd -match "rm\s+-[rf]{1,2}\s+[\/\\]" -or $cmd -match "git\s+reset\s+--hard" -or $cmd -match "del\s+\/s\s+\/q\s+[c-z]:\\" -or $cmd -match "drop\s+database") {
        $response = @{
            decision = "deny"
            reason = "[BLOCK 400: Destructive Command Intercepted] Irreversible command '$cmd' is blocked by Antigravity Safety Guard."
        }
        $response | ConvertTo-Json -Compress
        exit 0
    }
}

# Passed all pre-tool guards
@{ decision = "allow" } | ConvertTo-Json -Compress
exit 0
