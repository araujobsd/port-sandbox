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

class JailsBuildStatus(object):

    @cherrypy.expose
    def index(self, JailId, ByResult):

        psb = psbdatabase.Select()
        jailresult = psb.ShowStatusByJail(JailId, ByResult)
        jailname = psb.JailName(None)
        start = Start()
        header = start.header()
        footer = start.footer()

        Dict = {"JailResult":jailresult, "JailName":jailname}
        html = Template(file="jailresult.tmpl", searchList=[Dict])

        yield header
        yield str(html)
        yield '<center>'
        yield footer
        yield '</center>'


class Jails(object):

    @cherrypy.expose
    def index(self):

        psb = psbdatabase.Select()
        jailinfo = psb.JailInfo()
        portsfail= psb.AllPortsStatus(1)
        portsok= psb.AllPortsStatus(0)
        start = Start()
        header = start.header()
        footer = start.footer()

        yield header

        # Code here
        Dict = {"Jails":jailinfo, "PortsFail":portsfail, "PortsOk":portsok}
        html = Template(file="jails.tmpl", searchList=[Dict])

        yield str(html)


        yield '<center>'
        yield footer
        yield '</center>'

class NoBuild(object):

    @cherrypy.expose
    def index(self):

        NoBuild = porterror.HandleErrors()
        result = NoBuild.NoBuild()
        start = Start()
        header = start.header()
        footer = start.footer()

        yield header
        yield str(result)
        yield footer



class AllPortsInQueue(object):


    @cherrypy.expose
    def AddPort(self, jail, port):

        PortDir = '/usr/ports/' + str(port)
        if os.path.isdir(PortDir):
            os.system("cd ../scripts/ ; ./init.py add %s %s" % (port, jail))

        raise cherrypy.InternalRedirect('/allportsinqueue/')

    @cherrypy.expose
    def RunPort(self):

        Pid = os.path.isfile("/tmp/portsandbox.lock")
        if Pid == True:
            print "It's running..."
        else:
            os.system("cd ../scripts/ ; ./portsandbox.py &")

        raise cherrypy.InternalRedirect('/allportsinqueue/')

    @cherrypy.expose
    def DelPort(self, IdPort):

        psb = psbdatabase.Select()
        psb.DelPort(IdPort)
        raise cherrypy.InternalRedirect('/allportsinqueue/')

    @cherrypy.expose
    def index(self):

        psb = psbdatabase.Select()
        start = Start()
        header = start.header()
        footer = start.footer()
        result = psb.AllPortsInQueue()
        jailname = psb.JailName(None)

        yield header
        yield '''
            <center><table width=800>
            <right><td align="right">

            <form action="AddPort" method="post">
            <b>Jail: </b>
            <select name="jail">
        '''
        for names in jailname:
            yield '<option value="%s">%s</option>' \
                    % (names[0], names[1])

        yield '''
            </select>
            <b>Port: </b>
            <input type="text" name="port" value="category/port" />
            <input type="submit" value="Add">
            </right></td></center></table><p></p>

            </form>
        '''


        offset = 0

        try:
            if result[0]:
                offset = 1
        except:
            offset = 0

        if offset == 0:
            yield '<center><b>There is nothing...</b></center>'
            yield '<br></br>'
        else:
            yield '''
                <center><table width=800>
                <thead>
                <tr>
                    <th class="caption"> Jail </th>
                    <th class="caption"> Port Directory </th>
                    <th class="caption"> Position </th>
                    <th class="caption"></th>
                </tr>
                </thead>
                <tbody>
            '''
            count = 0
            for portId, port, jailid in result:
                count = count + 1
                yield '<tr>'
                yield '<td><center>' + str(psb.JailName(jailid)[0]) + '</center></td>'
                yield '<td><center>' + port + '</center></td>'
                yield '<td><center>' + str(count) + '</center></td>'
                yield '''<td><center><form action="DelPort" method="post">
                <input type="hidden" name="IdPort" value="%s">
                <input type="submit" value="Del"></form></center></td>''' % (portId)
                yield '</tr>'
            yield '</table>'

            yield '''
            <center><table width=800>
            <thread>
            <tr>
                <th class="caption"> When you're prepared to run the Port-Sandbox, click here.</th>
                <th class="caption">
            <right><form action="RunPort" method="post">
            <input type="submit" value="Run Port-Sandbox"></form></right>
            </th>
            </thread></table></center>
            '''

        yield '<center>'
        yield footer
        yield '</center>'


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
    nobuild = NoBuild()

    @cherrypy.expose
    def index(self, JailId):

        yield '<title> Test </title>'
        header = self.header()
        footer = self.footer()
        yield header
        psb = psbdatabase.Select()

        if JailId == None:
            QueueResult = psb.Queue(None)
        else:
            QueueResult = psb.Queue(JailId)

        NextBuild = psb.NextInQueue()
        NextBuild = str(NextBuild[0])

        yield '''
            <center><table width=800 class='caption'>
            <td>Next port in queue:
        '''
        yield '''<a> <b>%s</b></a>''' % (NextBuild)
        yield '''
            <right><td align="right"><b>Legend:    </b>
                [ <a>Build OK: <img src="../images/green.png" alt="OK" width="15"/></a> ]
                [ <a>Build Error: <img src="../images/red.png" alt="ERROR" width="15"/></a> ]
                [ <a>Dependency Error: <img src="../images/yellow.png" alt="Dep Error" width="15"/></a> ]
                [ <a>Plist Error: <img src="../images/orange.png" alt="Plist Error" width="15"/></a> ]
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
                    BuildError = DependsError.DependsErrors(Id[0], 'BuildDepends')
                    RunError = DependsError.DependsErrors(Id[0], 'RunDepends')

                    LibSize = len(LibError)
                    BuildSize = len(BuildError)
                    RunSize = len(RunError)

                    ControlDepLibError = []
                    ControlDepBuildError = []
                    ControlDepRunError = []

                    if LibSize != 0:
                        for libError in LibError:
                            if libError[3] != 0 and libError[3] != None or libError[4] != 0 and libError[4] != None or \
                                    libError[5] != 0 and libError[5] != None or libError[6] != 0 and libError[6] != None:
                                        ControlDepError = 1
                                        ControlDepLibError.append(ControlDepError)
                            elif libError[3] == None or libError[4] == None or \
                                    libError[5] == None or libError[6] == None:
                                        ControlDepError = 2
                                        ControlDepLibError.append(ControlDepError)
                            elif libError[3] == 0 and libError[4] == 0 and \
                                    libError[5] == 0 and libError[6] == 0:
                                        ControlDepError = 0
                                        ControlDepLibError.append(ControlDepError)

                    if BuildSize != 0:
                        for buildError in BuildError:
                            if buildError[3] != 0 and buildError != None  or buildError[4] != 0 and buildError != None or \
                                    buildError[5] != 0 and buildError != None or buildError[6] != 0 and buildError != None:
                                        ControlDepError = 1
                                        ControlDepBuildError.append(ControlDepError)
                            elif buildError[3] == None or buildError[4] == None or \
                                    buildError[5] == None or buildError[6] == None:
                                        ControlDepError = 2
                                        ControlDepBuildError.append(ControlDepError)
                            elif buildError[3] == 0 and buildError[4] == 0 and \
                                    buildError[5] == 0 and buildError[6] == 0:
                                        ControlDepError = 0
                                        ControlDepBuildError.append(ControlDepError)

                    if RunSize != 0:
                        for runError in RunError:
                            if runError[3] != 0 and runError != None or runError[4] != 0 and runError[4] != None or \
                                    runError[5] != 0 and runError[5] != None or runError[6] != 0 and runError[6] != None:
                                        ControlDepError = 1
                                        ControlDepRunError.append(ControlDepError)
                            elif runError[3] == None or runError[4] == None or \
                                    runError[5] == None or runError[6] == None:
                                        ControlDepError = 2
                                        ControlDepRunError.append(ControlDepError)
                            elif runError[3] == 0 and runError[4] == 0 and \
                                    runError[5] == 0 and runError[6] == 0:
                                        ControlDepError = 0
                                        ControlDepRunError.append(ControlDepError)

                    # Check if the MainPort are OK to show the green daemon.
                    MainPort = psbdatabase.Select()
                    mainPort = MainPort.MainPort(Id[0])
                    MainPortError = 0
                    MainPortNotFinished = 0
                    Status = 0

                    # Check if there is any dependencie with problem and
                    # set ControlDepError equal 1
                    for error in ControlDepLibError:
                        if error == 1:
                            ControlDepError = 1

                    for error in ControlDepRunError:
                        if error == 1:
                            ControlDepError = 1

                    for error in ControlDepBuildError:
                        if error == 1:
                            ControlDepError =1


                    # If there is no dependencies
                    try:
                        ControlDepError
                    except:
                        ControlDepError = 3


                    if mainPort[3] != 0 or mainPort[4] != 0 or mainPort[5] != 0 or \
                            mainPort[6] != 0 or mainPort[7] != 0 or \
                            mainPort[8] != 0 or mainPort[9] != 0:
                                MainPortError = 1
                    elif mainPort[3] == None or mainPort[4] == None or \
                            mainPort[5] == None or mainPort[6] == None or \
                            mainPort[7] == None or mainPort[8] == None or \
                            mainPort[8] == None or mainPort[9] == None:
                                MainPortError = 2

                    if mainPort[11] == 0:
                        PlistError = 0
                    elif mainPort[11] == 256 or mainPort[11] == 512:
                        PlistError = 1
                    elif mainPort[11] == None:
                        PlistError = 2


                    if MainPortError == 1 and ControlDepError == 2 and PlistError == 2 or \
                            MainPortError == 1 and ControlDepError == 0 and PlistError == 2 or \
                            MainPortError == 1 and ControlDepError == 3 and PlistError == 2:
                        Status = '<img src="../images/red.png" alt="ERROR" width="15"/>'

                    if MainPortError == 0 and ControlDepError == 0 and PlistError == 0 or \
                        MainPortError == 0 and ControlDepError == 2  and PlistError == 0 or MainPortError == 0 and ControlDepError == 3 and PlistError == 0:
                        Status = '<img src="../images/green.png" alt="OK" width="15"/>'

                    if MainPortError == 1 and ControlDepError == 1 and PlistError == 2 or MainPortError == 1 and ControlDepError == 3 and PlistError == 1:
                        Status = '<img src="../images/yellow.png" alt="DEPS ERROR" width="15"/>'

                    if MainPortError == 0 and ControlDepError == 0 and PlistError == 1 or MainPortError == 0 and ControlDepError == 3 and PlistError == 1 or MainPortError == 1 and ControlDepError == 0 and PlistError == 1 or MainPortError == 1 and ControlDepError == 3 and PlistError == 1:
                            Status = '<img src="../images/orange.png" alt="PLIST ERROR" width="15"/>'

                    yield '''
                        <tr>
                            <td><center>%s</center></td>
                            <td><center><a href="/start/?JailId=%s">%s</a></center></td>
                            <td><center><a href="%s">%s</a></center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center>%s</center></td>
                            <td><center><A href="/pageerror/?Id=%s" title="Teste">log</A></center></td>
                        </tr>
                    ''' % (Committer, JailId[0], JailId[0], Id[2], Port, PortVersion[:-1], \
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

class Index(object):


    allportsinqueue = AllPortsInQueue()
    pageerror = PageError()
    nobuild = NoBuild()
    start = Start()
    jails = Jails()
    jailsbuildstatus = JailsBuildStatus()

    @cherrypy.expose
    def index(self):

        raise cherrypy.InternalRedirect('/start/?JailId=None')


cherrypy.config.update('prod.conf')
cherrypy.quickstart(Index(),config="app.conf")
cherrypy.engine.start()
