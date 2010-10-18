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
            <center><table width='90%' class='caption'>
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
            <center><table width="90%">
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
                    ControlDepError = 0

                    for libError in LibError:
                        if libError[3] != 0 or libError[4] != 0 or \
                                libError[5] != 0 or libError[6] != 0 or \
                                libError[7] != 0: ControlDepError = 1

                    for buildError in BuilError:
                        if buildError[3] != 0 or buildError[4] != 0 or \
                                buildError[5] != 0 or buildError[6] != 0 or \
                                buildError[7] != 0: ControlDepError = 1

                    for runError in RunError:
                        if runError[3] != 0 or runError[4] != 0 or \
                                runError[5] != 0 or runError[6] != 0 \
                                : ControlDepError = 1

                    # Check if the MainPort are OK to show the green daemon.
                    MainPort = psbdatabase.Select()
                    mainPort = MainPort.MainPort(Id[0])
                    MainPortError = 0
                    PlistError = 0

                    if mainPort[3] != 0 or mainPort[4] != 0 or mainPort[5] != 0 or \
                            mainPort[6] != 0 or mainPort[7] != 0 or \
                            mainPort[8] != 0 or mainPort[9] != 0: MainPortError = 1
                    if mainPort[11] != 0:
                        PlistError = 1


                    if MainPortError == 1 and ControlDepError == 0:
                        Status = '<img src="images/red.png" alt="ERROR" width="15"/>'
                    if MainPortError == 0 and ControlDepError == 0 and \
                            PlistError == 0:
                        Status = '<img src="images/green.png" alt="OK" width="15"/>'
                    if ControlDepError == 1:
                        Status = '<img src="images/yellow.png" alt="DEPS ERROR" width="15"/>'
                    if PlistError == 1 and ControlDepError == 0:
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
                            <td><center><b><A href="/pageerror/?Id=%s" title="Teste">log</b></A></center></td>
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
