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
