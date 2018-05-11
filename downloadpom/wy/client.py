#coding=utf-8  
import requests  
import os
url = "http://127.0.0.1:8080"  
# path = os.getcwd()+"/handle_pom.py"
# print(path)
# files = {'file': open(path, 'rb')}
# //org.apache.tomcat/tomcat-jdbc/
# m_data = {"groupId":"org.apache.tomcat","artifactId":"tomcat-jdbc","version":"9.0.8","id":260}
m_data = {"groupId":"org.wildfly.core","artifactId":"wildfly-core-parent","version":"5.0.0.Alpha4","id":285};
# files = {'file':open(path,'rb')}
# r = requests.post(url, files=files)
r = requests.post(url, data=m_data)
print(r.url)
print(r.text)