#coding=utf-8  
from http.server import BaseHTTPRequestHandler  
import cgi
from handle_pom import get_pom
class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,  
            headers=self.headers,  
            environ={'REQUEST_METHOD':'POST',  
                     'CONTENT_TYPE':self.headers['Content-Type'],  
                     }  
        )  

        groupId = None
        artifactId = None
        version = None
        for field in form.keys():  
            field_item = form[field]  
            key = field_item.name
            value  = field_item.value
            # filesize = len(filevalue)#文件大小(字节)
            #print len(filevalue)  
            # print(key)
            if key == 'artifactId':
                artifactId = value
            if key == 'groupId':
                groupId = value
            if key == 'version':
                version = value
            # print(value)
            # with open(filename+".txt",'wb') as f:
            #     f.write(filevalue)
        if groupId != None and artifactId != None and version != None:
            content = get_pom(groupId, artifactId, version)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(('Client: %sn \n' % str(self.client_address)).encode())
        self.wfile.write(('User-agent: %sn\n' % str(self.headers['user-agent'])).encode())
        self.wfile.write(('Path: %sn\n'%self.path).encode())
        self.wfile.write(('Form data:n\n').encode())
        self.wfile.write('File:fileName.pom\n'.encode())
        self.wfile.write(content)
        return  
  
def StartServer():
    print('server started')
    from http.server import HTTPServer  
    sever = HTTPServer(("",8080),PostHandler)  
    sever.serve_forever()  
  
  
  
  
if __name__=='__main__':  
    StartServer()  