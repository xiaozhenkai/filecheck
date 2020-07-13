* fc目录为filecheck，需要先建立索引再设置crontab定期扫描。
    * 下载对应脚本
        * `curl https://github.com/xiaozhenkai/filecheck/raw/master/fc/fc.py > fc.py`
    * 先整理出需要加入监控的文件列表,例子里的默认目录是home/wwwroot/web/，以Discuz论坛为例
        * `cd /home/wwwroot/web/ ; find . -name '*.php' | egrep -v 'log|data/template|cache_study_keyword|cache'  | tee ~/php.list`
    * 生成md5索引
        * `python -B fc.py buildDb /home/wwwroot/web/ php.list`
    * crontab定期检查
        * `* * * * * python -B fc.py c /home/wwwroot/web/`
    * 修改文件列表
        * `vi php.list 或 find 重新输出`
    * 当文件变更后需要重新建立索引
        * `python -B fc.py buildDb /home/wwwroot/web/ php.list`
* safe目录为discuz专用的php脚本执行权限过滤
    * 下载safe.php以及whitelist放置在/tmp目录
        * 也可以是其他目录，比如/var/lib/php比/tmp更安全。
        * 这里如果是amh需要注意chroot，需要搞到对应网站目录的tmp或者var目录。
        * `chattr +i safe.php`
        
    * 修改php.ini
        
        * php.ini中添加`auto_prepend_file = /tmp/safe.php`
        
    * 维护whitelist文件
    
    * 对称混淆【实际可以解密】
    
        * ```php
            $text = '
            $arr = explode(PHP_EOL,file_get_contents(__DIR__."/whitelist"));
            array_pop($arr);
            if ( !in_array($_SERVER["SCRIPT_NAME"],$arr) ){
                    header("HTTP/1.1 403 Forbidden");
                    exit();
            }';
            
            $encoded = base64_encode(str_rot13(gzdeflate($text)));
            
            print_r($encoded);
            ```
    
            
    
    * 去除了mobcent目录的特殊逻辑，后续mobcent需要使用如下指令添加到whitelist
        
        * `find mobcent/ -name "*.php"| sed 's/^/\//g' >> whitelist`
* 其他待添加