import socket
import os

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('IP_Address', 'Port'))
    
    
    
    filename = raw_input("Enter name of file or 'q' to quit: ")
    if filename == 'q':
        s.close()
        
    else:
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            print "Would you like to:"
            print "1) Download file"
            print "2) Add a new record "
            print "3) Show student info by ID"
            print "4) Find students by score"
            print "5) Show all information for students"
            print "6) Delete a student's record by ID"
            print "7) Exit."
                
            message = raw_input("Enter: ")
                
        if message == "1":
            s.send('OK')
            f = open('new_'+filename,'wb')
            data = s.recv(1024)
            totalRecv = len(data)
            f.write(data)
                
            while totalRecv < filesize:
                data = s.recv(1024)
                totalRecv += len(data)
                f.write(data)
                    
            print "Download Complete"
                
        if message == "2":
            s.send('ADD')
            ID = raw_input("ID: ")
            s.send(ID)
            fname = raw_input("First name: ")
            s.send(fname)
            lname = raw_input("Last name: ")
            s.send(lname)
            score = raw_input("Score: ")
            s.send(score)
                
                    
        if message == "3":
            s.send('ID')
            idNum = raw_input("Enter the student's ID: ")
            s.send(idNum)
            
            data = s.recv(1024)
            filesize = long(data)
                               
            fileData = s.recv(1024)
            totalRecv = len(fileData)
            print fileData
                               
            while totalRecv < filesize:
                fileData = s.recv(1024)
                totalRecv += len(fileData)
                print fileData
                               
            print "End of student's info."
            
        if message == "4":
            s.send('SCORE')
            score = raw_input("Enter a score for displaying students' info: ")
            s.send(score)
            data = s.recv(1024)
            filesize = long(data)
                
            fileData = s.recv(1024)
            totalRecv = len(fileData)
            print fileData
                
            while totalRecv < filesize:
                fileData = s.recv(1024)
                totalRecv += len(fileData)
                print fileData
                
            print "EOF"
                
                
        if message == "5":
            s.send('ALL')
            printFile = s.recv(1024)
            print "Printing on client side: "
            print printFile
                
        if message == "6":
            s.send('RMV')
                
            idNum = raw_input("Enter the student's ID you wish to delete: ")
            s.send(idNum)
                
            data = s.recv(1024)
            filesize = long(data)
                                      
            fileData = s.recv(1024)
            totalRecv = len(fileData)
            print fileData
                                      
            while totalRecv < filesize:
                fileData = s.recv(1024)
                totalRecv += len(fileData)
                print fileData
                                      
            print "Deletion Completed."
                
        if message == "7":
            s.close()
    
  
if __name__ == '__main__':
        main()
                
