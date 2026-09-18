# -*- coding: utf-8 -*-
# engine/sdd/run_gate.ps1
# Unified CLI Runner for SDD Deterministic Gatekeeper Pipeline

param (
    [Parameter(Mandatory=$true)]
    [string]$Id,

    [Parameter(Mandatory=$false)]
    [string]$Gate,

    [Parameter(Mandatory=$false)]
    [string]$Step,

    [switch]$Approve,

    [switch]$Assert,

    [string]$Notes = ""
)

$PythonBat = "C:\Program Files\QGIS 3.44.12\bin\python-qgis-ltr.bat"
$EngineDir = "$PSScriptRoot"

if ($Approve) {
    if (-not $Step) { $Step = "gate$Gate" }
    & $PythonBat "$EngineDir\assert_approval.py" --action issue --id $Id --step $Step --notes $Notes
    exit $LASTEXITCODE
}

if ($Assert) {
    if (-not $Step) { $Step = "gate$Gate" }
    & $PythonBat "$EngineDir\assert_approval.py" --action assert --id $Id --step $Step
    exit $LASTEXITCODE
}

if ($Gate -eq "1") {
    & $PythonBat "$EngineDir\verify_gate1.py" --id $Id
    exit $LASTEXITCODE
}

if ($Gate -eq "2") {
    & $PythonBat "$EngineDir\verify_gate2.py" --id $Id
    exit $LASTEXITCODE
}

if ($Step -eq "qgis") {
    & $PythonBat "$EngineDir\verify_qgis_map.py" --id $Id
    exit $LASTEXITCODE
}

Write-Host "Usage: .\engine\sdd\run_gate.ps1 -Id <id> [-Gate 1|2] [-Step qgis] [-Approve] [-Assert] [-Notes <text>]"
exit 1
