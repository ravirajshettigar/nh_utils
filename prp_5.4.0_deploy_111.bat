set "path=C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Development\maven\bin;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files (x86)\Microsoft SQL Server\110\DTS\Binn\;C:\Program Files\TortoiseSVN\bin;c:\Program Files\Microsoft SQL Server\110\DTS\Binn\;C:\Carefx\Resources\hsip-base-5.3.5-SNAPSHOT\bin;C:\Development\Git\bin;C:\Development\Python27;C:\Development\nvm;C:\Development\nodejs;C:\Users\rshettigar\AppData\Roaming\npm;C:\Development\nvm;C:\Development\nodejs;C:\Users\rshettigar\AppData\Local\Programs\Fiddler;C:\Development\maven\bin;C:\Program Files\Java\jdk1.7.0_80\bin"
set "java_home=C:\Program Files\Java\jdk1.7.0_80"
set "catalina_home=C:\Development\servers\apache_tomcat_prp"
set "maven_home=C:\Development\maven"
set "maven_opts=-Xms512m -Xmx2048m -XX:MaxPermSize=512m"
set "carefx_home=C:\PrP_Carefx"
set "servicemix_home=C:\PrP_Carefx\Resources\hsip"
set "catalina_opts=-Dcarefx.props.dir=%CAREFX_HOME%\Common\properties -Dcarefx.common.dir=%CAREFX_HOME%\Common -Dcarefx.cfgprop.impl=net.carefx.config.filesystem.impl.CfgPropertiesImpl -XX:MaxPermSize=512m -Xms1024m -Xmx2048m"
set "karaf_opts="
set "catalina_opts=%catalina_opts% -DproxySet=true -Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=9999"
set "karaf_opts=%karaf_opts% -DproxySet=true -Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=9999"
set "catalina_opts=%catalina_opts% -Xdebug -Xrunjdwp:transport=dt_socket,address=4711,server=y,suspend=n"
set "karaf_opts=%karaf_opts% -Xdebug -Xrunjdwp:transport=dt_socket,address=5711,server=y,suspend=n"
del /f /s /q C:\PrP_Carefx\Resources\hsip\data\log\*
del /f /s /q C:\PrP_Carefx\Resources\hsip\Carefx\Common\logs\*
cd /d C:\PrP_Carefx\Resources\hsip\bin
start servicemix
del /f /s /q C:\Development\servers\apache_tomcat_prp\logs\*
rmdir /s /q C:\Development\servers\apache_tomcat_prp\work\Catalina
cd /d C:\Development\servers\apache_tomcat_prp\bin
start catalina.bat run
