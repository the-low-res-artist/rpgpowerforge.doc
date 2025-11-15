<?php

function LogMessage($message)
{
	global $logfile;
	$logfile = 'updateDocs.log';
	$time = time();
	$date = date('Y-m-d H:i:s');
	file_put_contents($logfile, $date . ': ' . $message . "\n", FILE_APPEND);
}

function updateSite()
{

        LogMessage("==========================================");
        LogMessage("Receiving push event, pull reposistory...");
        $result = shell_exec('whoami && pwd && cd .. && git reset --hard origin/main && git clean -fd && git fetch && git pull');
        LogMessage($result);

        LogMessage("Update building scripts rights...");
	$result = shell_exec('chmod -R 777 ./../.. 2>&1');
	LogMessage($result);

	LogMessage("Run build scripts...");
        $result = shell_exec('cd .. && ./rebuild_website.sh 2>&1');
        LogMessage($result);
}

$input = file_get_contents('php://input');
$json = json_decode($input);

if (!is_null($json))
{
	updateSite();
}
?>
