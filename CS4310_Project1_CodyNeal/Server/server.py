import socket
import threading
import os
import readline

def add(c,file):
    print "at add"
    studentID = c.recv(1024)
    studentFName = c.recv(1024)
    studentLName = c.recv(1024)
    studentScore = c.recv(1024)
    
    with open(file, 'a') as f:
        f.write(studentID + "\t"+ studentFName + "\t" +\
        studentLName + "\t" + studentScore)
        f.write("\n")
        
        
        
def displayID(c,file):
    print "at ID"
    idNum = c.recv(1024)
    
    with open(file, 'r') as f:
           s = ' '
           while(s):
               s = f.readline()
               field = s.split("\t")
               if len(s) > 0:
                   if (field[0]) == idNum:
                       
                       with open('tempfile.txt', 'w') as t:
                           studentID = field[0]
                           t.write(studentID + "\t")
                           
                           studentFName = field[1]
                           t.write(studentFName + "\t")
                           
                           studentLName = field[2]
                           t.write(studentLName + "\t")
                           
                           studentScore = field[3]
                           t.write(studentScore + "\n")
                      
                           t.close()
           f.close()
           
    with open('tempfile.txt','rb') as t:
           filesize = str(os.path.getsize('tempfile.txt'))
           c.send(filesize)
                           
           bytesToSend = t.read(1024)
           c.send(bytesToSend)
           while bytesToSend != "":
               bytesToSend = t.read(1024)
               c.send(bytesToSend)
           t.close()
           
    if os.path.exists("tempfile.txt"):
        os.remove("tempfile.txt")
    else:
        print("The file does not exist")
            
def displayScore(c,file):
    print "at score"
    score = c.recv(1024)
    print score
    with open(file, 'r') as f:
        s = ' '
        while(s):
            s = f.readline()
            field = s.split("\t")
            if len(s) > 0:
                if (field[3]) > score:
                    
                    with open('tempfile.txt', 'w') as t:
                        studentID = field[0]
                        t.write(studentID + "\t")
                        
                        studentFName = field[1]
                        t.write(studentFName + "\t")
                        
                        studentLName = field[2]
                        t.write(studentLName + "\t")
                        
                        studentScore = field[3]
                        t.write(studentScore + "\n")
                   
                        t.close()
        f.close()
        
    with open('tempfile.txt','rb') as t:
        filesize = str(os.path.getsize('tempfile.txt'))
        c.send(filesize)
                        
        bytesToSend = t.read(1024)
        c.send(bytesToSend)
        while bytesToSend != "":
            bytesToSend = t.read(1024)
            c.send(bytesToSend)
        t.close()
        
    if os.path.exists("tempfile.txt"):
        os.remove("tempfile.txt")
    else:
      print("The file does not exist")
      
      
        
def displayAll(c,file):
    print "at all"
    c.send(file)
                    
def deleteRecord(c,file):
    print "at delete"
        
    idNum = c.recv(1024)
          
    with open(file, 'rt') as f:
        temp = open('tempfile.txt', 'wt')
        s = ' '
        while(s):
            s = f.readline()
            field = s.split("\t")
            if len(s) > 0:
                if (field[0]) != idNum:
                    temp.write(s)
    f.close()
    temp.close()
    
    with open('tempfile.txt','rb') as t:
           filesize = str(os.path.getsize('tempfile.txt'))
           c.send(filesize)
                           
           bytesToSend = t.read(1024)
           c.send(bytesToSend)
           while bytesToSend != "":
               bytesToSend = t.read(1024)
               c.send(bytesToSend)
           t.close()
    
    if os.path.exists(file):
           os.remove(file)
    else:
        print("The file does not exist")
         
    if os.path.exists("tempfile.txt"):
           os.rename("tempfile.txt",file)
    else:
        print("The file does not exist")
    
def requests(name, sock):
        filename = sock.recv(1024)
        if (filename):
            sock.send("EXISTS " + str(os.path.getsize(filename)))
            userResponse = sock.recv(1024)
            if userResponse[:2] == 'OK':
                    with open(filename,'rb') as f:
                        bytesToSend = f.read(1024)
                        sock.send(bytesToSend)
                        while bytesToSend != "":
                                bytesToSend = f.read(1024)
                                sock.send(bytesToSend)
                                
            if userResponse[:3] == 'ADD':
                add(sock,filename)

            if userResponse[:2] == 'ID':
                displayID(sock,filename)
            
            if userResponse[:5] == 'SCORE':
                displayScore(sock,filename)
                
            if userResponse[:3] == 'ALL':
                with open(filename,'rb') as f:
                    file_data = f.read(1024)
                    f.close()
                    displayAll(sock,file_data)
                
            if userResponse[:3] == 'RMV':
                deleteRecord(sock,filename)
                
        else:
            sock.send("ERR")
    
        sock.close()
 



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('IP_ADDR', PORT))

    s.listen(5)
    print "Socket is listening"

    while True:
        c, address = s.accept()
        print 'Got connection from', address
        t = threading.Thread(target=requests, args=("reqThread",c))
        t.start()
    
    s.close()

if __name__ == '__main__':
        main()

