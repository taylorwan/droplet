#####################################
# drop.let
# hophacks spring'15
#####################################

from dropbox.client import DropboxClient
from dropbox.session import DropboxSession

import dropbox
import sys
import urllib

from bs4 import BeautifulSoup
import urllib2

presentWorkingDirectory = '/'

class Commands(object):
    def listFiles(self, arrayOfCommand, client):
        directories = currentFolders(client)
        documents = currentFiles(client)
        
        sms = "Folders: "
        for directory in directories:
            sms += "\n" + directory
        sms += "\n\nFiles: "
        for document in documents:
            sms += "\n" + document
            
        return sms
    
    def makeFile(self, arrayOfCommand, client):
        f= open("vim.txt", 'w')
        fileName=arrayOfCommand[2]
        if fileInFolder(fileName, client ):
           return "It seems that \"" + fileName +  "\" already exists!"
        path = presentWorkingDirectory + fileName
        newFile = open(fileName,'w')
        f.write("we got here")
        if len(arrayOfCommand)>3:
            content = " ".join(arrayOfCommand[3:])
            newFile.write( content )
            newFile.close()

        f = open(fileName,'rb')
        fileCreated = client.put_file(path, f)
        if not fileCreated:
            print "It seems that something has gone wrong!"
        print "File " + fileName + " created!"

    def getFile(self, arrayOfCommand, client):
        return ""

    def makeFolder(self, arrayOfCommand, client):
        folderName = getNameOfFolderAndFile( arrayOfCommand )
        if folderInFolder( folderName, client ):
            return "It seems that \"" + folderName +  "\" already exists!"
       
        path = presentWorkingDirectory + folderName
        folderCreated = client.file_create_folder( path )
        if not folderCreated:
            return "It seems that something has gone wrong!"
        return "Folder " + folderName + " created!"

    def moveFolder(self, arrayOfCommand, client):
        global presentWorkingDirectory
        if len(arrayOfCommand) == 4:
            folderToMove = arrayOfCommand[2]
            folderToMove.replace("\"", "")
            folderToMove.replace("\'","")
            if folderInFolder(folderToMove, client):
                pathToMoveTo = arrayOfCommand[3]
                try:
                    print presentWorkingDirectory[1:]+folderToMove
                    client.file_copy(presentWorkingDirectory+folderToMove, pathToMoveTo)
                    arrayOfCommand[2]= presentWorkingDirectory[1:]+folderToMove
                    arrayOfCommand = arrayOfCommand[:-1] 
                    self.removeFolder(arrayOfCommand, client)
                except:
                    return "There is an error we will code this later"
                return "Successfully moved the folder " + presentWorkingDirectory + folderToMove + " to " + pathToMoveTo
            else:
                return "The file " + folderToMove + "does not exist"
        else:
            return "Syntax Error"

    def moveFile(self, arrayOfCommand, client):
        global presentWorkingDirectory
        if len(arrayOfCommand) == 4:
            fileToMove = arrayOfCommand[2]
            fileToMove.replace("\"", "")
            fileToMove.replace("\'","")
            if fileInFolder(fileToMove, client):
                pathToMoveTo = arrayOfCommand[3]
                try:
                    client.file_copy(presentWorkingDirectory+fileToMove, pathToMoveTo)
                    arrayOfCommand[2] = presentWorkingDirectory[1:]+fileToMove
                    arrayOfCommand = arrayOfCommand[:-1] 
                    self.removeFile(arrayOfCommand, client)
                except:
                    return "Unsuccessful"
                return "Successfully moved the file "+ presentWorkingDirectory +""+ fileToMove + " to " + pathToMoveTo
            else:
                return "The file " + fileToMove + "does not exist"
        else:
            return "Syntax Error"

    def renameFile(self, arrayOfCommand, client):
        if len(arrayOfCommand) != 4:
            raise Exception ("Syntax error")
        arrayOfCommand[2] = presentWorkingDirectory[1:] + arrayOfCommand[2]
        arrayOfCommand[3] = presentWorkingDirectory[1:] + arrayOfCommand[3]
        return self.moveFile(arrayOfCommand, client )
        
    def renameFolder(self, arrayOfCommand, client):
        if len(arrayOfCommand) != 4:
            raise Exception ("Syntax error")
        arrayOfCommand[2] = presentWorkingDirectory[1:] + arrayOfCommand[2]
        arrayOfCommand[3] = presentWorkingDirectory[1:] + arrayOfCommand[3]
        return self.moveFolder( arrayOfCommand, client )
        
    def removeFolder(self, arrayOfCommand, client):
        folderName = getNameOfFolderAndFile( arrayOfCommand )
        path = presentWorkingDirectory + folderName
        if not folderInFolder( folderName, client ):
            return folderName + " doesn't exist in this folder!"
        folderDeleted = client.file_delete( path )
        if folderDeleted['is_deleted'] == True:
            return folderName + " successfully deleted!"
        return folderName + " successfully deleted!"

    def removeFile(self, arrayOfCommand, client):
        fileName = getNameOfFolderAndFile( arrayOfCommand )
        path = presentWorkingDirectory + fileName
        if not fileInFolder( fileName, client ):
            return fileName + " doesn't exist in this folder!"
        fileDeleted = client.file_delete( path )
        if fileDeleted['is_deleted'] == True:
            return fileName + " successfully deleted!"
        return fileName + " successfully deleted!"


    def changeDirectory(self, arrayOfCommand, client):
        global presentWorkingDirectory 
        newDirectory = getNameOfFolderAndFile(arrayOfCommand)
        if folderInFolder(newDirectory, client):
            presentWorkingDirectory += newDirectory + "/"
            return "You are now in " + newDirectory
        else:
            return "I'm sorry, " + newDirectory + " does not exist"
        

    def shareFile(self, arrayOfCommand, client):
        fileName = arrayOfCommand[2].replace("\"","").replace("\'","")
        receipient = arrayOfCommand[3]
        path = presentWorkingDirectory + fileName
        if not fileInFolder( fileName, client ):
            return fileName + " doesn't exist in this folder!"
        shareData = client.share(path, short_url=True)
        shortURL = shareData['url']
        return "Sent " + shortURL + " to " + receipient
    
    def shareFolder(self, arrayOfCommand, client):
        folderName = arrayOfCommand[2].replace("\"","").replace("\'","")
        receipient = arrayOfCommand[3].replace("-'","")
        path = presentWorkingDirectory + folderName
        if not folderInFolder( folderName, client ):
            return folderName + " doesn't exist in this folder!"
        shareData = client.share(path, short_url=True)
        shortURL = shareData['url']
        return "Sent " + shortURL + " to " + receipient
    
    def getMostRecent(self, arrayOfCommand, client):
        arrayOfCommand.remove(arrayOfCommand[0])
        arrayOfCommand.remove(arrayOfCommand[0])
        for command in arrayOfCommand:
            found = searchFromRoot( command, client )
            if found:
                return found
        


# end of commands class

# global functions
def getNameOfFolderAndFile(arrayOfCommand):
    if len(arrayOfCommand) > 3:
        arg = "".join(arrayOfCommand[2:len(arrayOfCommand)])
    else:
        if len(arrayOfCommand) == 3:
            arg = arrayOfCommand[2].replace('\'','').replace('\"','')
        else:
            return "Syntax Error"
    return arg
        
def getCurrentMeta( client, path = presentWorkingDirectory ):
     return client.metadata( path )

def currentFolders(client, path = presentWorkingDirectory ):
    folder_metadata = getCurrentMeta(client)
    directories = []
    for file in folder_metadata['contents']:
        name = file['path'].replace('/','') 
        if file['is_dir'] == True :
            directories.append(name)
    return directories

def currentFiles( client, path=presentWorkingDirectory ):
    folder_metadata = getCurrentMeta(client)
    files = []
    for file in folder_metadata['contents']:
        name = file['path'].replace('/','')
        if file['is_dir'] == False :
            files.append(name)
    return files

def fileInFolder(fileName, client):
    files = currentFiles(client)
    for file in files:
        if file == fileName:
            return True
    return False

def folderInFolder(folderName, client):
    folders = currentFolders(client)
    for folder in folders:
        if folder == folderName:
            return True
    return False

def searchFromRoot( fileName, client ):
    foundFile = searchFiles( fileName, client, "/" )
    if foundFile == -1:
        return "No files matching " + fileName + " found."
    return foundFile

def searchFiles( fileName, client, path ):
    files = currentFiles( client, path )
    for someFile in files:
        if someFile.find( fileName ) != -1:
            path += someFile
            shareData = client.share(path, short_url=True)
            url = shareData['url'] 

            # Beautiful Soup setup
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page.read(), 'html.parser')
            content = soup.select("#preview-img")[0].get('src')
            return content

    # file not in current directory! let's dive deeper
    folders = currentFolders(client)
    if not folders:
        return -1
    for folder in folders:
        searchFiles( fileName, client, path+folder )


def getFunctionCall(command):
    return {
        'listfiles': "listFiles",
        'ls': "listFiles",
        'makefile': "makeFile",
        'getfile': "getFile",
        'makefolder': "makeFolder",
        'mkdir': "makeFolder",
        'removefolder': "removeFolder",
        'rmdir': "removeFolder",
        'removefile': "removeFile",
        'rm': "removeFile",
        'movefile': "moveFile",
        'mv': "moveFile",
        'movefolder': "moveFolder",
        'changedirectory' : "changeDirectory",
        'cd' : "changeDirectory",
        'sharefile': "shareFile",
        'sendfile': "shareFile",
        'sharefolder': "shareFolder",
        'sendfolder': "shareFolder",
        'renamefile': "renameFile",
        'renamefolder': "renameFolder",
        'gettag': "getMostRecent",
        }.get(command, "Syntax Error")


def placeHolderRemover(command):
    placeholders = ["with","to"]
    for placeholder in placeholders:
        command.replace(placeholder,"")
            
def get_token(phone_num="9737474259"):
    filename = "numbersToTokens.txt"
    phone_num=phone_num[-10:]
    f = open(filename, 'r')
    for line in f:
        tokens = line.split("|")
        if phone_num == tokens[0]:
            return tokens[1][:-1]
    return False

def photo(path, client):
    imgFile=open(path, 'r')
    newFileName=path.rsplit('/', 1)[1]
    client.put_file(newFileName, imgFile)
    print 'success'

def inputString():
    global arrayOfCommand
    phoneNumber = sys.argv[2]
    f=open("vim.txt", "w")
    f.write("we are at least in main") 
    client = dropbox.client.DropboxClient(get_token(phoneNumber), locale=None, rest_client=None)
    f.write("now here")
    if len(sys.argv)>3:
      print sys.argv
      photo(sys.argv[3], client)
    else:
        stringInput = sys.argv[1]

        easter = ["cd","mkdir","ls","mv","rmdir","rm"]
        placeholders = ["with","to"]

        arrayOfCommand = stringInput.split()
        
        for command in reversed(arrayOfCommand):
            if command in placeholders:
                arrayOfCommand.remove(command)
          
        command = arrayOfCommand[0]
        if command in easter:
            arrayOfCommand.insert(0,"")
        command = arrayOfCommand[0] + arrayOfCommand[1]
        methodName = getFunctionCall(command.lower())

        my_cls = Commands()
        method = getattr(my_cls, methodName)

        if not method:
            return "Syntax Error"

        print method(arrayOfCommand, client)

inputString()

#def printAnything():
#    print "anything"
#printAnything()
# DropboxClient(oauth2_access_token, locale=None, rest_client=None)

# inputString("share folder derp with with to to taylor")
# inputString("get tag derp")
