﻿filter leftside{
param(
 [Parameter(Position=0, Mandatory=$true,ValueFromPipeline = $true)]
 [ValidateNotNullOrEmpty()]
 [PSCustomObject]
 $obj
 )
 $obj|?{$_.sideindicator -eq '=>'}
}
Compare-Object (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\warehouse_logfiles\warehouse_log1.txt") (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\sensor_logfiles\log-sensor1.txt") |
leftside
Compare-Object (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\warehouse_logfiles\warehouse_log1.txt") (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\sensor_logfiles\log-sensor2.txt") |
leftside
Compare-Object (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\warehouse_logfiles\warehouse_log1.txt") (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\sensor_logfiles\log-sensor3.txt") |
leftside
echo "=> nicht in lager-log"
echo "<= nicht ind sensor-log wird nicht angezeigt, da sonst die ausgabe vollgemüllt ist"
$serverNumber = (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\warehouse_logfiles\warehouse_log1.txt").Count
$sensorNumber = (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\sensor_logfiles\log-sensor1.txt").Count
$sensorNumber += (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\sensor_logfiles\log-sensor2.txt").Count
$sensorNumber += (Get-Content "D:\UNI\Aktuelles_Semester\Verteilte_Systeme_WS21\VS_Python\sensor_logfiles\log-sensor3.txt").Count
$difference = $serverNumber - $sensorNumber
echo "Es gibt $difference zu viele oder wenige Einträge in der Server-log"
echo "Anzahl der Einträge aus allen Sensoren $sensorNumber"
Read-Host -Prompt "Press Enter to exit"
