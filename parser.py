from dropbox.client import DropboxClient
from dropbox.session import DropboxSession

presentWorkingDirectory = '/'

# commands class

class Commands(object):
    def listFiles(self, arrayOfCommand, client):
        documents = currentFolders(client)
        directories = currentFiles(client)
        
        sms = "Folders: "
        for directory in directories:
            sms += "\n" + directory
        sms += "\n\nFiles: "
        for document in documents:
            sms += "\n" + document
            
        return sms

    
    def makeFile(self, arrayOfCommand, client):
        getNameOfFolderAndFile(arrayOfCommand)
        return ""

    def getFile(self, arrayOfCommand, client):
        return ""


    def makeFolder(self, arrayOfCommand, client):
        folderName = getNameOfFolderAndFile( arrayOfCommand )
        if folderInFolder( folderName ):
            return "It seems that \"" + folderName +  "\" already exists!"
        
        path = presentWorkingDirectory + folderName
#         folderCreated = client.file_create_folder( path )
        folderCreated = "creating folder " + folderName + " at path: " + path
        if not folderCreated:
            return "It seems that something has gone wrong!"
        return "Folder " + folderName + " created!"


    def moveFolder(self, arrayOfCommand, client):
        arrayOfCommand.replace("to","")
        print "we are here2"
        global presentWorkingDirectory
        if len(arrayOfCommand) == 4:
            print "here in if"
            folderToMove = arrayOfCommand[2]
            folderToMove.replace("\"", "")
            folderToMove.replace("\'","")
            if folderInFolder(folderToMove):
                pathToMoveTo = arrayOfCommand[3]
                try:
                    # file_copy(presentWorkingDirectory+folderToMove, pathToMoveTo)
                    print "something"
                except:
                    return "There is an error we will code this later"
                return "Successfully moved the folder " + presentWorkingDirectory + folderToMove + " to " + pathToMoveTo
            else:
                return "The file " + folderToMove + "does not exist"
        else:
            raise Exception ("Syntax funcking error")

    def moveFile(self, arrayOfCommand, client):
        arrayOfCommand.remove("to")
        print "we are here2"
        global presentWorkingDirectory
        if len(arrayOfCommand) == 4:
            print "here in if"
            fileToMove = arrayOfCommand[2]
            fileToMove.replace("\"", "")
            fileToMove.replace("\'","")
            if fileInFolder(fileToMove):
                pathToMoveTo = arrayOfCommand[3]
                try:
                    # file_copy(presentWorkingDirectory+fileToMove, pathToMoveTo)
                    print "something"
                except:
                    return "There is an error we will code this later"
                return "Successfully moved the file "+ presentWorkingDirectory +""+ fileToMove + " to " + pathToMoveTo
            else:
                return "The file " + fileToMove + "does not exist"
        else:
            raise Exception ("Syntax funcking error")


    def renameFile(self, arrayOfCommand, client):
        if arrayOfCommand != 4:
            raise Exception ("Syntax error")
        arrayOfCommand[2] = presentWorkingDirectory + arrayOfCommand[2]
        arrayOfCommand[3] = presentWorkingDirectory + arrayOfCommand[3]
        return moveFile( self, arrayOfCommand, client )
        

    def renameFolder(self, arrayOfCommand, client):
        if arrayOfCommand != 4:
            raise Exception ("Syntax error")
        arrayOfCommand[2] = presentWorkingDirectory + arrayOfCommand[2]
        arrayOfCommand[3] = presentWorkingDirectory + arrayOfCommand[3]
        return moveFolder( self, arrayOfCommand, client )
        
        
        
        
    def removeFolder(self, arrayOfCommand, client):
        folderName = getNameOfFolderAndFile( arrayOfCommand )
        path = presentWorkingDirectory + folderName
        if not folderInFolder( folderName ):
            return folderName + " doesn't exist in this folder!"
#         folderDeleted = client.file_delete( path )
        folderDeleted = {"size": "0 bytes","is_deleted": True,"bytes": 0,"thumb_exists": False,"rev": "1f33043551f","modified": "Wed, 10 Aug 2011 18:21:30 +0000","path": "/test","is_dir": False,"icon": "page_white_text","root": "dropbox","mime_type": "text/plain","revision": 492341}
        if folderDeleted['is_deleted'] == True:
            return folderName + " successfully deleted!"
        return folderName + " successfully deleted!"
#         return "Error: " + folderName + "not deleted"

    def removeFile(self, arrayOfCommand, client):
        fileName = getNameOfFolderAndFile( arrayOfCommand )
        path = presentWorkingDirectory + fileName
        if not fileInFolder( fileName ):
            return fileName + " doesn't exist in this folder!"
#         fileDeleted = client.file_delete( path )
        fileDeleted = {"size": "0 bytes","is_deleted": True,"bytes": 0,"thumb_exists": False,"rev": "1f33043551f","modified": "Wed, 10 Aug 2011 18:21:30 +0000","path": "/test .txt","is_dir": False,"icon": "page_white_text","root": "dropbox","mime_type": "text/plain","revision": 492341}
        if fileDeleted['is_deleted'] == True:
            return fileName + " successfully deleted!"
        return fileName + " successfully deleted!"
#         return "Error: " + fileName + "not deleted"


    def changeDirectory(self, arrayOfCommand, client):
    # def changeDirectory(self,arrayOfCommand):
        global presentWorkingDirectory 
        newDirectory = getNameOfFolderAndFile(arrayOfCommand)
        if folderInFolder(newDirectory):
            presentWorkingDirectory += newDirectory + "/"
            return "You are now in " + newDirectory
        else:
            return "I'm sorry, " + newDirectory + " does not exist"
        

    def shareFile(self, arrayOfCommand, client):
        fileName = arrayOfCommand[2].replace("\"","").replace("\'","")
        receipient = arrayOfCommand[3]
        path = presentWorkingDirectory + fileName
        if not fileInFolder( fileName ):
            return fileName + " doesn't exist in this folder!"
#         shareData = client.share(path, short_url=True)
        shareData = {'url': u'https://db.tt/c0mFuu1Y', 'expires': 'Tue, 01 Jan 2030 00:00:00 +0000'}
        shortURL = shareData['url']
        return "Sending " + shortURL + " to " + receipient
    
    def shareFolder(self, arrayOfCommand, client):
    # def shareFolder(self, arrayOfCommand):
        folderName = arrayOfCommand[2].replace("\"","").replace("\'","")
        receipient = arrayOfCommand[3].replace("-'","")
        path = presentWorkingDirectory + folderName
        if not folderInFolder( folderName ):
            return folderName + " doesn't exist in this folder!"
#         shareData = client.share(path, short_url=True)
        shareData = {'url': u'https://db.tt/c0mFuu1Y', 'expires': 'Tue, 01 Jan 2030 00:00:00 +0000'}
        shortURL = shareData['url']
        return "Sending " + shortURL + " to " + receipient

# end of commands class

    
# global functions
def getNameOfFolderAndFile(arrayOfCommand):
    if len(arrayOfCommand) > 3:
        arg = "".join(arrayOfCommand[2:len(arrayOfCommand)])
    else:
        if len(arrayOfCommand) == 3:
            arg = arrayOfCommand[2].replace('\'','').replace('\"','')
        else:
            raise Exception ("Syntax funcking error")

        return arg
        
def getCurrentMeta(client):
#     return client.metadata( presentWorkingDirectory )
    return {'bytes': 0,'contents': [{'bytes': 0,'icon': 'folder','is_dir': True,'modified': 'Thu, 25 Aug 2011 00:03:15 +0000','path': '/droplets','rev': '803beb471','revision': 8,'root': 'dropbox','size': '0 bytes','thumb_exists': False},{'bytes': 77,'icon': 'page_white_text','is_dir': False,'mime_type': 'text/plain','modified': 'Wed, 20 Jul 2011 22:04:50 +0000','path': '/droplets.txt','rev': '362e2029684fe','revision': 221922,'root': 'dropbox','size': '77 bytes','thumb_exists': False}],'hash': 'efdac89c4da886a9cece1927e6c22977','icon': 'folder','is_dir': True,'path': '/','root': 'app_folder','size': '0 bytes','thumb_exists': False}
 
def currentFolders(client):
    folder_metadata = getCurrentMeta(client)
    directories = []
    for file in folder_metadata['contents']:
        name = file['path'].replace('/','')
        if file['is_dir'] == True :
            directories.append(name)
    return directories

def currentFiles(client):
    folder_metadata = getCurrentMeta(client)
    files = []
    for file in folder_metadata['contents']:
        name = file['path'].replace('/','')
        if file['is_dir'] == False :
            files.append(name)
    return files

def fileInFolder(fileName):
    files = currentFiles(client)
    for file in files:
        if file == fileName:
            return True
    return False

def folderInFolder(folderName):
    folders = currentFolders(client)
    for folder in folders:
        if folder == folderName:
            return True
    return False


def getFunctionCall(command):
    return {
        'listfiles': "listFiles",
        'ls': "listFiles",
        'makefile': "makeFile",
        'getfile': "getFile",
        'makefolder': "makeFolder",
        'mkdir': "makeDirectory",
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
        'sharefolder': "shareFolder",
        'renamefile': "renameFile",
        'renamefolder': "renameFolder",
        }.get(command, "this is a fucking syntax error")


def placeHolderRemover(command):
    placeholders = ["with","to"]
    for placeholder in placeholders:
        command.replace(placeholder,"")
            

def inputString(stringEntered):
    global arrayOfCommand
    
    stringInput=stringEntered
    easter = ["cd","mkdir","ls","mv","rmdir","rm"]
    placeholders = ["with","to"]

    arrayOfCommand = stringInput.split()
        

    for command in reversed(arrayOfCommand):
        if command in placeholders:
            arrayOfCommand.remove(command)
            
    if len(arrayOfCommand)<2:
        raise Exception("Syntax error")
    else: 
        command = arrayOfCommand[0]
        if command in easter:
            arrayOfCommand.insert(0,"")
        command = arrayOfCommand[0] + arrayOfCommand[1]
        methodName = getFunctionCall(command.lower())

    my_cls = Commands()
    method = getattr(my_cls, methodName)

    if not method:
        raise Exception ("Syntax error")

    print method(arrayOfCommand)


inputString("Share folder droplets with Taylor")