import tornado.ioloop
import tornado.web
import os
import subprocess

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('NS3.html')
	

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        if self.request.files:
            myfile = self.request.files['myfile'][0]
            fin = open("ns-3-allinone/ns-3-dev/scratch/test.cc","w")  
            fin.write(myfile["body"])
            fin.close()

            #info=os.popen('cd ns-3-allinone/ns-3-dev/;./waf;./waf --run scratch/test','r')
            #print(info.read())
            #self.write(info[1].read())


            p=subprocess.Popen('cd ns-3-allinone/ns-3-dev/;./waf;./waf --run scratch/test', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            p3=subprocess.Popen('java -jar tracemetrics.jar',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            p2=subprocess.Popen('cd ns-3-allinone/ns-3-dev/;cp test.tr ../../static', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #print (p.stdout.readlines())
            self.write('<html><body>'
            '<h1 style="font-size:170%;color:green">The Results Indication</h1>'
            '<p style="font-family:verdana;font-size:130%">'+p.stdout.read()+'</p></body></html>')
           
            #for line in p.stdout.readlines():
           # print line
            #retval=p.wait()
           
         


settings = {
"static_path": os.path.join(os.path.dirname(__file__), "static") 
}
application=tornado.web.Application([(r'/',MainHandler),(r'/upload', UploadHandler) ],**settings)

if __name__=='__main__':
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
