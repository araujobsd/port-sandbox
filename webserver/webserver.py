import cherrypy
import MySQLdb
import os.path
from Cheetah.Template import Template

database = MySQLdb.connect('localhost','root', '')
database.select_db('portsandbox')
cursor = database.cursor()
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))

class ResultFromDatabase():


    def init(self):

        PortsQueue, LibDepends = self.PortsInQueue()

        return PortsQueue, LibDepends


    def PortsInQueue(self):

        cmd = 'SELECT * FROM Queue'
        cursor.execute(cmd)
        Result = cursor.fetchall()
        ListDepends = []

        for result in Result:
            LibDepends = self.LibDepends(result[0])
            ListDepends.append(LibDepends)

        return Result, ListDepends

    def NextBuild(self):

        cmd = 'SELECT * From Queue'
        cursor.execute(cmd)
        Result = cursor.fetchall()
        Next = None

        for result in Result:
            if result[5] == 0 and Next == None:
                Next = result[1]

        return Next

    def LibDepends(self, Id):

        cmd = 'SELECT Id, PortName FROM LibDepends WHERE Id=%s' % (Id)
        cursor.execute(cmd)
        Result = cursor.fetchall()

        return Result


    def JailsName(self):

        cmd = 'SELECT Id, JailName FROM Jail'
        cursor.execute(cmd)
        Result = cursor.fetchall()

        return Result


    def MainPort(self):

        cmd = 'SELECT Id, PortLog FROM MainPort'
        cursor.execute(cmd)
        Result = cursor.fetchall()

        return Result



class Start(object):


    @cherrypy.expose
    def index(self):

        result = ResultFromDatabase()
        yield '<title> Test </title>'
        header = self.header()
        footer = self.footer()
        yield header
        MainPort = result.MainPort()
        PortsQueue, LibDepends = result.init()
        JailsName = result.JailsName()
        NextBuild = result.NextBuild()
        result = self.body(MainPort, PortsQueue, LibDepends, JailsName, NextBuild)
        yield str(result)
        yield footer

    def header(self):

        header = Template(file="header.tmpl")
        return str(header)


    def footer(self):

        footer = Template(file="footer.tmpl")
        return str(footer)


    def body(self, MainPort, PortsQueue, LibDepends, Jails, NextBuild):

        mp = {"MainPort":MainPort, "Queue":PortsQueue, "LibDepends":LibDepends,"Jails":Jails, "NextBuild":NextBuild}
        test = Template(file="body.tmpl", searchList=[mp])
        return test





cherrypy.config.update('prod.conf')
cherrypy.quickstart(Start(),config="app.conf")
cherrypy.engine.start()
