<#
1. Creates logs for:
    - Login attempts by Michael Tan, Rachel Simmons, and Dr. Wong.
    - Failed login attempts and privilege escalations.

2. Generates logs with realistic but inconsistent timestamps.
  
3. Simulates log tampering to hide traces of actual events.

Relation to the Attack Scenario:
    - Reflects Michael Tan's efforts to hide his after-hours access and remote logins.
    - Generates fake events to confuse investigators and obscure the timeline of the attack.
#>

$Users = @("Michael Tan", "Rachel Simmons", "Dr. Wong")
$EventIDs = @(4624, 4625, 4648)
$IPs = @("192.168.1.105", "10.0.0.54", "203.0.113.25")

For ($i=0; $i -lt 500; $i++) {
    $User = $Users | Get-Random
    $IP = $IPs | Get-Random
    $EventID = $EventIDs | Get-Random
    $Time = (Get-Date).AddMinutes(-($i * 5))
    Write-EventLog -LogName "Security" -Source "AuditLog" -EventId $EventID `
        -EntryType Information -Message "User $User logged in from IP $IP at $Time."
}
