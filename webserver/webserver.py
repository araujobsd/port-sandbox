import cherrypy
import MySQLdb
import os.path
from Cheetah.Template import Template
import psbdatabase

database = MySQLdb.connect('localhost','root', '')
database.select_db('portsandbox')
cursor = database.cursor()
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))

class PageError(object):


    @cherrypy.expose
    def index(self):
        return "Page Error...."


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
            <td>Next in the Pool:
        '''
        yield '''<a> <b>%s</b></a>''' % (NextBuild)
        yield '''
            <right><td align="right"><b>Legend:    </b>
                [ <a>Build OK: <img src="images/green.png" alt="OK" width="15"/></a> ]
                [ <a>Build Error: <img src="images/red.png" alt="ERROR" width="15"/></a> ]
                [ <a>Dependency Error: <img src="images/yellow.png" alt="Dep Error" width="15"/></a> ]
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
            </tr>
            </thead>
            <tbody>
        '''

        for result in QueueResult:
            if result[5] == 1:
                Id = psb.MainPort(result[0])
                Committer = Id[10]
                Port = result[1]
                Date = result[4]
                LibDependsQuant = psb.DependsQuant("LibDepends", Id[0])
                BuildDependsQuant = psb.DependsQuant("BuildDepends", Id[0])
                RunDependsQuant = psb.DependsQuant("RunDepends", Id[0])

                PortVersion = Id[2].split('/')
                PortVersion = PortVersion[3].split('log')
                PortVersion = PortVersion[0]
                Status = result[2]
                JailId = psb.JailName(result[3])

                if Status == 1:
                    Status = '<img src="images/red.png" alt="ERROR" width="15"/>'
                if Status == 0:
                    Status = '<img src="images/green.png" alt="OK" width="15"/>'

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
                    </tr>
                ''' % (Committer, JailId[0], Id[2], Port, PortVersion[:-1], \
                        LibDependsQuant, BuildDependsQuant, RunDependsQuant, Date, Status)


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
