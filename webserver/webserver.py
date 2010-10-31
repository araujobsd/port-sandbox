import cherrypy
import MySQLdb
import os.path
from Cheetah.Template import Template
import psbdatabase
import porterror

database = MySQLdb.connect('localhost','root', '')
database.select_db('portsandbox')
cursor = database.cursor()
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))

class AllPortsInQueue(object):

    @cherrypy.expose
    def index(self):
        psb = psbdatabase.Select()
        start = Start()
        header = start.header()
        footer = start.footer()
        result = psb.AllPortsInQueue()
        yield header
        yield str(result)
        yield footer


class PageError(object):


    @cherrypy.expose
    def index(self, Id):
        PortErrors = porterror.HandleErrors()
        Result = PortErrors.MainPortErrors(Id)
        start = Start()
        header = start.header()
        footer = start.footer()
        yield header
        yield Result
        yield footer


class Start(object):

    allportsinqueue = AllPortsInQueue()
    pageerror = PageError()

    @cherrypy.expose
    def index(self):

        yield '<title> Test </title>'
        header = self.header()
        footer = self.footer()
        yield header
        psb = psbdatabase.Select()
        QueueResult = psb.Queue()
        NextBuild = psb.NextInQueue()
        NextBuild = str(NextBuild[0])

        yield '''
            <center><table width=800 class='caption'>
            <td>Next port in queue:
        '''
        yield '''<a> <b>%s</b></a>''' % (NextBuild)
        yield '''
            <right><td align="right"><b>Legend:    </b>
                [ <a>Build OK: <img src="images/green.png" alt="OK" width="15"/></a> ]
                [ <a>Build Error: <img src="images/red.png" alt="ERROR" width="15"/></a> ]
                [ <a>Dependency Error: <img src="images/yellow.png" alt="Dep Error" width="15"/></a> ]
                [ <a>Plist Error: <img src="images/orange.png" alt="Plist Error" width="15"/></a> ]
                </right>

            '''
        yield '</td></td></center></table><p></p>'

        yield '''
            <center><table width=800>
            <thead>
            <tr>
                <th class="caption"> Committer </th>
                <th class="caption"> Jail </th>
                <th class="caption"> Port Directory </th>
                <th class="caption"> Version </th>
                <th class="catpion"> L </th>
                <th class="caption"> B </th>
                <th class="caption"> R </th>
                <th class="caption"> Date </th>
                <th class="caption"> Status </th>
                <th class="caption"> Details </th>
            </tr>
            </thead>
            <tbody>
        '''

        for result in QueueResult:
            if result[5] == 1:
                Id = psb.MainPort(result[0])
                if Id:
                    Committer = Id[10]
                    Port = result[1]
                    Date = result[4]
                    LibDependsQuant = psb.DependsQuant("LibDepends", Id[0])
                    BuildDependsQuant = psb.DependsQuant("BuildDepends", Id[0])
                    RunDependsQuant = psb.DependsQuant("RunDepends", Id[0])

                    PortVersion = Id[2].split('/')
                    PortVersion = PortVersion[3].split('log')
                    PortVersion = PortVersion[0]
                    JailId = psb.JailName(result[3])

                    # Check if there is any dependency with error.
                    # Set the yellow daemon then.
                    DependsError = porterror.HandleErrors()
                    LibError = DependsError.DependsErrors(Id[0], 'LibDepends')
                    BuilError = DependsError.DependsErrors(Id[0], 'BuildDepends')
                    RunError = DependsError.DependsErrors(Id[0], 'RunDepends')

                    for libError in LibError:
                        if libError[3] == 1 or libError[4] == 1 or \
                                libError[5] == 1 or libError[6] == 1:
                                    ControlDepError = 1
                        elif libError[3] == None or libError[4] == None or \
                                libError[5] == None or libError[6] == None:
                                    ControlDepError = 2
                        elif libError[3] == 0 and libError[4] == 0 and \
                                libError[5] == 0 and libError[6] == 0:
                                    ControlDepError = 0

                    for buildError in BuilError:
                        if buildError[3] == 1 or buildError[4] == 1 or \
                                buildError[5] == 1 or buildError[6] == 1:
                                    ControlDepError = 1
                        elif buildError[3] == None or buildError[4] == None or \
                                buildError[5] == None or buildError[6] == None:
                                    ControlDepError = 2
                        elif buildError[3] == 0 and buildError[4] == 0 and \
                                buildError[5] == 0 and buildError[6] == 0:
                                    ControlDepError = 0

                    for runError in RunError:
                        if runError[3] == 1 or runError[4] == 1 or \
                                runError[5] == 1 or runError[6] == 1 \
                                : ControlDepError = 1
                        elif runError[3] == None or runError[4] == None or \
                                runError[5] == None or runError[6] == None:
                                    ControlDepError = 2
                        elif runError[3] == 0 and runError[4] == 0 and \
                                runError[5] == 0 and runError[6] == 0:
                                    ControlDepError = 0

                    # Check if the MainPort are OK to show the green daemon.
                    MainPort = psbdatabase.Select()
                    mainPort = MainPort.MainPort(Id[0])
                    MainPortError = 0
                    MainPortNotFinished = 0
                    Status = 0

                    # If there is no dependencies
                    try:
                        ControlDepError
                    except:
                        ControlDepError = 3

                    if mainPort[3] != 0 or mainPort[4] != 0 or mainPort[5] != 0 or \
                            mainPort[6] != 0 or mainPort[7] != 0 or \
                            mainPort[8] != 0 or mainPort[9] != 0: MainPortError = 1
                    elif mainPort[3] == None or mainPort[4] == None or \
                            mainPort[5] == None or mainPort[6] == None or \
                            mainPort[7] == None or mainPort[8] == None or \
                            mainPort[8] == None or mainPort[9] == None:
                                MainPortError = 2


                    if mainPort[11] == 0:
                        PlistError = 0
                    elif mainPort[11] == 512:
                        PlistError = 1
                    elif mainPort[11] == None:
                        PlistError = 2

                    if MainPortError == 1 and ControlDepError == 2 and PlistError == 2 or \
                            MainPortError == 1 and ControlDepError == 0 and PlistError == 2:
                        Status = '<img src="images/red.png" alt="ERROR" width="15"/>'
                    if MainPortError == 0 and ControlDepError == 0 and PlistError == 0 or \
                        MainPortError == 0 and ControlDepError == 2  and PlistError == 0 or MainPortError == 0 and ControlDepError == 3 and PlistError == 0:
                        Status = '<img src="images/green.png" alt="OK" width="15"/>'
                    if MainPortError == 1 and ControlDepError == 1 and PlistError == 2:
                        Status = '<img src="images/yellow.png" alt="DEPS ERROR" width="15"/>'
                    if MainPortError == 0 and ControlDepError == 0 and PlistError == 1 or MainPortError == 0 and ControlDepError == 3 and PlistError == 1:
                        Status = '<img src="images/orange.png" alt="PLIST ERROR" width="15"/>'

                    yield '''
                        <tr>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center><a href="%s">%s</a></center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center><A href="/pageerror/?Id=%s" title="Teste">log</A></center></td>
                        </tr>
                    ''' % (Committer, JailId[0], Id[2], Port, PortVersion[:-1], \
                            LibDependsQuant, BuildDependsQuant, RunDependsQuant, Date,  Status, Id[0])


        yield '''
            </tbody></table>
        '''

        yield footer

    def header(self):

        header = Template(file="header.tmpl")
        return str(header)


    def footer(self):

        footer = Template(file="footer.tmpl")
        return str(footer)



cherrypy.config.update('prod.conf')
cherrypy.quickstart(Start(),config="app.conf")
cherrypy.engine.start()
