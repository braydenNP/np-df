$Users = @("Michael Tan", "Rachel Simmons", "Dr. Wong", "Susan Lee")
$EventIDs = @(4624, 4625, 4670)
$IPs = @("192.168.1.105", "10.0.0.54", "203.0.113.25", "198.51.100.14")

For ($i=0; $i -lt 500; $i++) {
    $User = $Users | Get-Random
    $IP = $IPs | Get-Random
    $EventID = $EventIDs | Get-Random
    $Time = (Get-Date).AddMinutes(-($i * 10))
    Write-EventLog -LogName "Security" -Source "AuditLog" -EventId $EventID `
        -EntryType Information -Message "User $User performed an action from IP $IP at $Time."
}
