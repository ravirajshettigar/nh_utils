set "path=C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files (x86)\Microsoft SQL Server\110\DTS\Binn\;C:\Program Files\TortoiseSVN\bin;c:\Program Files\Microsoft SQL Server\110\DTS\Binn\;C:\Carefx\Resources\hsip-base-5.3.5-SNAPSHOT\bin;C:\Development\Git\bin;C:\Development\Python27;C:\Development\nvm;C:\Development\nodejs;C:\Development\maven_3.5\bin;C:\Users\rshettigar\AppData\Roaming\npm;C:\Development\nvm;C:\Development\nodejs;C:\Users\rshettigar\AppData\Local\Programs\Fiddler;C:\Development\maven\bin;C:\Program Files\Java\jdk1.7.0_80\bin"
set "java_home=C:\Program Files\Java\jdk1.7.0_80"
setx /m java_home "C:\Program Files\Java\jdk1.7.0_80"
set "catalina_home=C:\PaP_Servers\v5.4.0\apache_tomcat"
setx /m catalina_home "C:\PaP_Servers\v5.4.0\apache_tomcat"
set "maven_home=C:\Development\maven"
setx /m maven_home "C:\Development\maven"
set "maven_opts=-Xms512m -Xmx2048m -XX:MaxPermSize=512m"
setx /m maven_opts "-Xms512m -Xmx2048m -XX:MaxPermSize=512m"
set "carefx_home=C:\PaP_Carefx"
setx /m carefx_home "C:\PaP_Carefx"
set "servicemix_home=C:\PaP_Carefx\v5.4.0\Resources\hsip-base-5.4.0-SNAPSHOT"
setx /m servicemix_home "C:\PaP_Carefx\v5.4.0\Resources\hsip-base-5.4.0-SNAPSHOT"
set "catalina_opts=-Dcarefx.props.dir=%CAREFX_HOME%\Common\properties -Dcarefx.common.dir=%CAREFX_HOME%\Common -Dcarefx.cfgprop.impl=net.carefx.config.filesystem.impl.CfgPropertiesImpl -XX:MaxPermSize=512m -Xms1024m -Xmx2048m"
setx /m catalina_opts "-Dcarefx.props.dir=%CAREFX_HOME%\Common\properties -Dcarefx.common.dir=%CAREFX_HOME%\Common -Dcarefx.cfgprop.impl=net.carefx.config.filesystem.impl.CfgPropertiesImpl -XX:MaxPermSize=512m -Xms1024m -Xmx2048m"
set "karaf_opts="
setx /m karaf_opts ""
set "catalina_opts=%catalina_opts% -DproxySet=true -Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=9999"
set "karaf_opts=%karaf_opts% -DproxySet=true -Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=9999"
set "catalina_opts=%catalina_opts% -Xdebug -Xrunjdwp:transport=dt_socket,address=4711,server=y,suspend=n"
set "karaf_opts=%karaf_opts% -Xdebug -Xrunjdwp:transport=dt_socket,address=5711,server=y,suspend=n"
cd /d "C:\PaP\v5.4.0\PaPRestServices"
svn update
cd /d "C:\PaP\v5.4.0\PatientPortal"
svn update
cd /d "C:\PaP\v5.4.0\PaPRestServices\Services\rest-services\providerdocument-service\providerdocument-service-api"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PaPRestServices\Services\rest-services\providerdocument-service\providerdocument-service-route"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PaPRestServices\Services\rest-services\reportactivity-service\reportactivity-service-api"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\common"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\install"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\patient-app"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\provider-app"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\services\adapters\registration-adapter"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\services\bundles\patient-portal-adapter-patient"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\webComponents\demograph-component"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\webComponents\messaging"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\webComponents\patientReport-component"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\webComponents\reportactivity-component"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\patient-app"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
cd /d "C:\PaP\v5.4.0\PatientPortal\provider-app"
mvn clean install -am -DVMachine=localhost -DskipTests=true dependency:sources
