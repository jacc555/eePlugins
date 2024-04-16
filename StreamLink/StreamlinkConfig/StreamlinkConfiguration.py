# -*- coding: utf-8 -*-
from __future__ import absolute_import #zmiana strategii ladowanie modulow w py2 z relative na absolute jak w py3
from Plugins.Extensions.StreamlinkConfig.__init__ import mygettext as _ , readCFG , DBGlog
from Plugins.Extensions.StreamlinkConfig.version import Version
from Plugins.Extensions.StreamlinkConfig.plugins.azmanIPTVsettings import get_azmanIPTVsettings
import os, time, sys
# GUI (Screens)
from Components.ActionMap import ActionMap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
#from Components.Sources.StaticText import StaticText
from enigma import eTimer, eConsoleAppContainer

from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Setup import SetupSummary


from emukodi.xbmcE2 import *

#### streamlink config /etc/streamlink/config ####
def getFFlist():
    ffList = []
    for f in sorted(os.listdir("/usr/bin"), key=str.lower):
        if f.startswith('ffmpeg'):
            ffList.append(("/usr/bin/%s" % f, f ))
    return ffList

def getCurrFF():
    ff = '/usr/bin/ffmpeg'
    for c in getStreamlinkConfig():
        if c.startswith('ffmpeg-ffmpeg='):
            tmp = c.split('=')[1].strip()
            if os.path.exists(tmp):
                ff = tmp
    return ff
    
def getStreamlinkConfig():
    try:
        cfg = open('/etc/streamlink/config', 'r').read().splitlines()
    except Exception:
        cfg = []
    return cfg

config.plugins.streamlinkSRV.streamlinkconfig = NoSave(ConfigNothing())
config.plugins.streamlinkSRV.streamlinkDRMconfig = NoSave(ConfigNothing())
config.plugins.streamlinkSRV.streamlinkEMUKODIconfig = NoSave(ConfigNothing())
config.plugins.streamlinkSRV.streamlinkconfigFFMPEG = NoSave(ConfigSelection(default = getCurrFF(), choices = getFFlist()))


class StreamlinkConfiguration(Screen, ConfigListScreen):
    from enigma import getDesktop
    if getDesktop(0).size().width() == 1920: #definicja skin-a musi byc tutaj, zeby vti sie nie wywalalo na labelach, inaczej trzeba uzywasc zrodla statictext
        skin = """<screen name="StreamlinkConfiguration" position="center,center" size="1000,700" title="Streamlink configuration">
                    <widget name="config"     position="20,20"   zPosition="1" size="960,600" scrollbarMode="showOnDemand" />
                    <widget name="key_red"    position="20,630"  zPosition="2" size="240,30" foregroundColor="red"    valign="center" halign="left" font="Regular;22" transparent="1" />
                    <widget name="key_green"  position="260,630" zPosition="2" size="240,30" foregroundColor="green"  valign="center" halign="left" font="Regular;22" transparent="1" />
                    <widget name="key_yellow" position="500,630" zPosition="2" size="240,30" foregroundColor="yellow" valign="center" halign="left" font="Regular;22" transparent="1" />
                    <widget name="key_blue"   position="740,630" zPosition="2" size="240,30" foregroundColor="blue"   valign="center" halign="left" font="Regular;22" transparent="1" />
                  </screen>"""
    else:
        skin = """<screen name="StreamlinkConfiguration" position="center,center" size="700,400" title="Streamlink configuration">
                    <widget name="config"     position="20,20" size="640,325" zPosition="1" scrollbarMode="showOnDemand" />
                    <widget name="key_red"    position="20,350" zPosition="2" size="150,30" foregroundColor="red" valign="center" halign="left" font="Regular;22" transparent="1" />
                    <widget name="key_green"  position="170,350" zPosition="2" size="150,30" foregroundColor="green" valign="center" halign="left" font="Regular;22" transparent="1" />
                    <widget name="key_yellow" position="360,350" zPosition="2" size="150,30" foregroundColor="yellow" valign="center" halign="left" font="Regular;22" transparent="1" />
                    <widget name="key_blue"   position="500,350" zPosition="2" size="150,30" foregroundColor="blue" valign="center" halign="left" font="Regular;22" transparent="1" />
                  </screen>"""
    def buildList(self):
        DBGlog('buildList >>> self.VisibleSection = %s' % self.VisibleSection )
        self.DoBuildList.stop()
        Mlist = []
        # pilot.wp.pl
        #Mlist.append(getConfigListEntry("", NoSave(ConfigNothing()) ))
        if not os.path.exists('/usr/sbin/streamlinkSRV'):
            Mlist.append(getConfigListEntry('\c00981111' + _("*** Deamon not installed ***")))
        else:
            Mlist.append(getConfigListEntry('\c00289496' + _("*** Available IPTV bouquets ***"), config.plugins.streamlinkSRV.One))
            if self.VisibleSection == 1:
                fileslist = []
                for f in sorted(os.listdir("/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/IPTVbouquets"), key=str.lower):
                    if f.startswith('OFF') or f.endswith('OFF') or f.endswith('OFF-not updated'):
                        pass
                    elif os.path.exists('/etc/enigma2/%s' % f):
                        fileslist.append(f)
                        Mlist.append(getConfigListEntry(_("Press OK to remove: %s") % f , config.plugins.streamlinkSRV.removeBouquet))
                    else:
                        Mlist.append(getConfigListEntry(_("Press OK to add: %s") % f , config.plugins.streamlinkSRV.installBouquet))
                for f in sorted(os.listdir("/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins"), key=str.lower):
                    if f.startswith('generate_') and f.endswith('.py'):
                        bname = f[9:-3]
                        if os.path.exists('/etc/enigma2/%s' % bname):
                            fileslist.append(bname)
                            Mlist.append(getConfigListEntry(_("Press OK to remove: %s") % bname , config.plugins.streamlinkSRV.removeBouquet))
                        else:
                            Mlist.append(getConfigListEntry(_("Press OK to create: %s") % bname , config.plugins.streamlinkSRV.generateBouquet))

                Mlist.append(getConfigListEntry('\c00009898' + _('Local IPTV bouquets')))
                #bukiety azman do wykluczenia
                for f in get_azmanIPTVsettings()['userbouquets']:
                    if os.path.exists('/etc/enigma2/%s' % f[1]):
                        fileslist.append(f[1])
                #budowanie listy
                for f in sorted(os.listdir("/etc/enigma2"), key=str.lower):
                    if f.startswith('userbouquet.') and f.endswith('.tv') and not 'azman' in f and not f in fileslist and not f in ['userbouquet.LastScanned.tv','userbouquet.WPPL.tv']:
                        DBGlog(f)
                        with open('/etc/enigma2/%s' % f, 'r') as fp:
                            try:
                                fpc = fp.read()
                            except Exception:
                                pass
                            fp.close()
                            services = fpc.count('#SERVICE ') - fpc.count('64:0:0:0:0:0:0:0:0::')
                            IPTVservices = services - fpc.count('::')
                            if IPTVservices > 0:
                                Mlist.append(getConfigListEntry(_("OK to change: %s with %s/%s IPTV services") % (f, IPTVservices, services) , config.plugins.streamlinkSRV.unmanagedBouquet))

            Mlist.append(getConfigListEntry(""))
            Mlist.append(getConfigListEntry('\c00289496' + _("*** %s configuration ***") % 'pilot.wp.pl', config.plugins.streamlinkSRV.Two))
            if self.VisibleSection == 2:
                Mlist.append(getConfigListEntry(_("Username:"), config.plugins.streamlinkSRV.WPusername))
                Mlist.append(getConfigListEntry(_("Password:"), config.plugins.streamlinkSRV.WPpassword))
                Mlist.append(getConfigListEntry(_("Check login credentials"), config.plugins.streamlinkSRV.WPlogin))
                #Mlist.append(getConfigListEntry("Przedstaw się jako:", config.plugins.streamlinkSRV.WPdevice))
                Mlist.append(getConfigListEntry(_("Prefer DASH than HLS:"), config.plugins.streamlinkSRV.WPpreferDASH))
                #Mlist.append(getConfigListEntry(_("Delay video:"), config.plugins.streamlinkSRV.WPvideoDelay))
                Mlist.append(getConfigListEntry(_("Press OK to create %s bouquet") % "userbouquet.WPPL.tv", config.plugins.streamlinkSRV.WPbouquet))
        
            if os.path.islink('/usr/sbin/streamlinkSRV') and 'StreamlinkConfig/' in os.readlink('/usr/sbin/streamlinkSRV'):
                if 1: # https://github.com/azman26
                    Mlist.append(getConfigListEntry(""))
                    Mlist.append(getConfigListEntry('\c00289496' + _("*** azman IPTV lists from github ***"),config.plugins.streamlinkSRV.Three))
                    if self.VisibleSection == 3:
                        azman = get_azmanIPTVsettings()['userbouquets']
                        for f in sorted(azman):
                            fUrl = f[0]
                            bname = _('%s (%s)') % (f[1], f[2])
                            if os.path.exists('/etc/enigma2/%s' % f[1]):
                                Mlist.append(getConfigListEntry(_("Press OK to remove: %s") % f[1] , config.plugins.streamlinkSRV.removeBouquet))
                            else:
                                Mlist.append(getConfigListEntry(_("Press OK to download: %s") % bname , config.plugins.streamlinkSRV.downloadBouquet, fUrl))
            
                else:
                    Mlist.append(getConfigListEntry(""))
                    Mlist.append(getConfigListEntry('\c00289496' + _("*** remote E2 helper ***"), config.plugins.streamlinkSRV.Three))
                    if self.VisibleSection == 3:
                        Mlist.append(getConfigListEntry(_("IP address:"), config.plugins.streamlinkSRV.remoteE2address))
                        Mlist.append(getConfigListEntry(_("Streaming port:"), config.plugins.streamlinkSRV.remoteE2port))
                        Mlist.append(getConfigListEntry(_("Username:"), config.plugins.streamlinkSRV.remoteE2username))
                        Mlist.append(getConfigListEntry(_("Password:"), config.plugins.streamlinkSRV.remoteE2password))
                        Mlist.append(getConfigListEntry(_("Wakeup if remote E2 in standby:"), config.plugins.streamlinkSRV.remoteE2wakeup))
                        Mlist.append(getConfigListEntry(_("Zap before stream workarround:"), config.plugins.streamlinkSRV.remoteE2zap))
        
                Mlist.append(getConfigListEntry(""))
                Mlist.append(getConfigListEntry('\c00289496' + _("*** Deamon configuration ***"), config.plugins.streamlinkSRV.Four))
                if self.VisibleSection == 4 or config.plugins.streamlinkSRV.enabled.value == False:
                    Mlist.append(getConfigListEntry(_("Enable deamon:"), config.plugins.streamlinkSRV.enabled))
                    Mlist.append(getConfigListEntry(_("Port number (127.0.0.1:X):"), config.plugins.streamlinkSRV.PortNumber))
                    Mlist.append(getConfigListEntry(_("Log level:"), config.plugins.streamlinkSRV.logLevel))
                    Mlist.append(getConfigListEntry(_("Log to file:"), config.plugins.streamlinkSRV.logToFile))
                    Mlist.append(getConfigListEntry(_("Clear log on each start:"), config.plugins.streamlinkSRV.ClearLogFile))
                    Mlist.append(getConfigListEntry(_("Save log file in:"), config.plugins.streamlinkSRV.logPath))
                    Mlist.append(getConfigListEntry(_("Buffer path:"), config.plugins.streamlinkSRV.bufferPath))
                    Mlist.append(getConfigListEntry(_("Allow Wrappers in lists:"), config.plugins.streamlinkSRV.useWrappers))
                    #Mlist.append(getConfigListEntry(_("Autocorrect framework for Wrappers:"), config.plugins.streamlinkSRV.Verify4Wrappers))
                    #EXPERIMENTAL OPTIONS
                    #Mlist.append(getConfigListEntry(_(" !!! EXPERIMENTAL OPTION(S) !!!")))
                   
                    #Mlist.append(getConfigListEntry(_("Recorder mode:"), config.plugins.streamlinkSRV.Recorder))
                    #if config.plugins.streamlinkSRV.Recorder.value == True:
                    #    Mlist.append(getConfigListEntry(_("Maximum record time:"), config.plugins.streamlinkSRV.RecordMaxTime))

                    #Mlist.append(getConfigListEntry(_("Refresh Generated bouquets in standby:"), config.plugins.streamlinkSRV.RefreshGeneratedBouquets))
                    
                    #Mlist.append(getConfigListEntry(_("IPTVExtMoviePlayer:// reacts on URL's with:"), config.plugins.streamlinkSRV.IPTVExtMoviePlayer))
                    
                    Mlist.append(getConfigListEntry(_("stop deamon on standby:"), config.plugins.streamlinkSRV.StandbyMode))

                    #Mlist.append(getConfigListEntry(_("Support VLC:"), config.plugins.streamlinkSRV.VLCusingLUA))
                    #Mlist.append(getConfigListEntry(_("Support KODI:"), config.plugins.streamlinkSRV.support4kodi))
                Mlist.append(getConfigListEntry(""))
                
                if config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value == '?':
                    Mlist.append(getConfigListEntry('\c00ff9400' + "*** Sprawdź dostępność wsparcia DRM ***", config.plugins.streamlinkSRV.Five))
                elif config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value == 'N':
                    Mlist.append(getConfigListEntry('\c00981111' + "*** Brak wsparcia DRM dla tej wersji pythona ***", config.plugins.streamlinkSRV.Five))
                elif config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value == 'K':
                    Mlist.append(getConfigListEntry('\c00981111' + "*** Brak wsparcia DRM, moduł emukodi nie zainstalowany ***", config.plugins.streamlinkSRV.Five))
                else:
                    if config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value == 'L':
                        Mlist.append(getConfigListEntry('\c00289496' + "*** Limitowane wsparcie DRM ***", config.plugins.streamlinkSRV.Five))
                    else:
                        Mlist.append(getConfigListEntry('\c00289496' + "*** Pełne wsparcie DRM ***", config.plugins.streamlinkSRV.Five))
                    for cfgFile in ['playermb']: #, 'canalplus', 'pgobox', 'cdaplMB', 'canalplusvod']:
                        if not os.path.exists('/etc/streamlink/%s' % cfgFile):
                            os.system('mkdir -p /etc/streamlink/%s' % cfgFile)
                    if self.VisibleSection == 5:
                        if 0: #cda
                            Mlist.append(getConfigListEntry('\c00981111' + _("*** cda not finished - no access anymore  ***")))
                            if os.path.exists('/etc/streamlink/cdaplmb/login') and os.path.exists('/etc/streamlink/cdaplmb/password') and \
                                open('/etc/streamlink/cdaplmb/login','r').read().strip() != '' and open('/etc/streamlink/cdaplmb/password','r').read().strip() != '':
                                    Mlist.append(getConfigListEntry( _("Press OK to create bouquet for") + ': cda' , config.plugins.streamlinkSRV.streamlinkDRMconfig))
                            else:
                                Mlist.append(getConfigListEntry( _("Missing configs for") + ' cda' , config.plugins.streamlinkSRV.streamlinkconfig))
                        if 1: #playerpl
                            if not os.path.exists('/etc/streamlink/playermb/refresh_token') or not os.path.exists('/etc/streamlink/playermb/logged') \
                                        or open('/etc/streamlink/playermb/refresh_token','r').read().strip() == '' \
                                        or open('/etc/streamlink/playermb/logged','r').read().strip() != 'true':
                                Mlist.append(getConfigListEntry('Logowanie do playerpl (w przeglądarce)' , config.plugins.streamlinkSRV.streamlinkEMUKODIconfig, ('playerpl', 'LOGIN')))
                            else:
                                Mlist.append(getConfigListEntry(_("Press OK to create %s bouquet") % "playerpl" , config.plugins.streamlinkSRV.streamlinkEMUKODIconfig, ('playerpl', 'userbouquet')))
                        if 0: #polsatgo
                            if os.path.exists('/etc/streamlink/polsatgo/login') and os.path.exists('/etc/streamlink/polsatgo/password'):
                                if open('/etc/streamlink/polsatgo/login','r').read().strip() != '' and open('/etc/streamlink/polsatgo/password','r').read().strip() != '':
                                    Mlist.append(getConfigListEntry( _("Press OK to create bouquet for") + ': polsatgo' , config.plugins.streamlinkSRV.streamlinkDRMconfig))
                            else:
                                Mlist.append(getConfigListEntry( _("Missing configs for") + ' polsatgo' , config.plugins.streamlinkSRV.streamlinkconfig))
                        if 0: #canal+
                            if os.path.exists('/etc/streamlink/canalplus/login') and os.path.exists('/etc/streamlink/canalplus/password') and os.path.exists('/etc/streamlink/canalplus/token'):
                                if open('/etc/streamlink/canalplus/login','r').read().strip() != '' and open('/etc/streamlink/canalplus/password','r').read().strip() != '':
                                    Mlist.append(getConfigListEntry( _("Press OK to create bouquet for") + ': canal+' , config.plugins.streamlinkSRV.streamlinkDRMconfig))
                            else:
                                Mlist.append(getConfigListEntry( _("Missing configs for") + ' canal+', config.plugins.streamlinkSRV.streamlinkconfig))
                        
            else:
                Mlist.append(getConfigListEntry(""))
                Mlist.append(getConfigListEntry('\c00981111' + _("*** not compliant Deamon found ***")))

        #Mlist.append()
        return Mlist

    def __init__(self, session, args=None):
        DBGlog('%s' % '__init__')
        self.doAction = None
        self.VisibleSection = 0
        if os.path.exists('/usr/sbin/streamlinkSRV') and os.path.islink('/usr/sbin/streamlinkSRV') and 'StreamlinkConfig/' in os.readlink('/usr/sbin/streamlinkSRV'):
            self.mySL = True
        else:
            self.mySL = False
        
        self.DoBuildList = eTimer()
        self.DoBuildList.callback.append(self.buildList)
        
        Screen.__init__(self, session)
        self.session = session

        # Summary
        self.setup_title = _("Streamlink Configuration" + ' v.' + Version)
        self.onChangedEntry = []

        # Buttons
        self["key_red"] = Label(_("Cancel"))
        
        if self.mySL == True:
            self["key_green"] = Label(_("Save"))
            self["key_blue"] = Label(_("Restart daemon"))
            if os.path.exists('/usr/lib/python2.7'):
                self["key_yellow"] = Label()
            elif os.path.exists('/tmp/streamlinkSRV.log'):
                self["key_yellow"] = Label(_("Show log"))
        else:
            self["key_green"] = Label()
            self["key_blue"] = Label()
            self["key_yellow"] = Label()

        # Define Actions
        self["actions"] = ActionMap(["StreamlinkConfiguration"],
            {
                "cancel":   self.exit,
                "red"   :   self.exit,
                "green" :   self.save,
                "yellow":   self.yellow,
                "blue"  :   self.blue,
                "save":     self.save,
                "ok":       self.Okbutton,
                "prevConf": self.prevConf,
                "nextConf": self.nextConf,
            }, -2)
        if 0:
            if not self.selectionChanged in self["config"].onSelectionChanged:
                self["config"].onSelectionChanged.append(self.selectionChanged)
        
        self.onLayoutFinish.append(self.layoutFinished)
        self.doAction = None
        ConfigListScreen.__init__(self, self.buildList(), on_change = self.changedEntry)

    def saveConfig(self):
        for x in self["config"].list:
            if len(x) >= 2:
                x[1].save()
        configfile.save()

    def save(self):
        if self.mySL == True:
            self.saveConfig()
            if os.path.exists('/var/run/streamlink.pid'):
                os.system('/etc/init.d/streamlinkSRV stop')
            if config.plugins.streamlinkSRV.enabled.value:
                os.system('/etc/init.d/streamlinkSRV start')
            self.VisibleSection = 0
            self.close(None)
        
    def refreshBuildList(self, ret = False):
        DBGlog('refreshBuildList >>>')
        self["config"].list = self.buildList()
        self.DoBuildList.start(50, True)
        
    def doNothing(self, ret = False):
        DBGlog('doNothing >>>')
        return
      
    def yellow(self):
        if self.mySL == True:
            if os.path.exists('/tmp/streamlinkSRV.log'):
                self.session.openWithCallback(self.doNothing ,Console, title = '/tmp/streamlinkSRV.log', cmdlist = [ 'cat /tmp/streamlinkSRV.log' ])
        
    def blue(self):
        if self.mySL == True:
            mtitle = _('Restarting daemon')
            cmd = '/usr/sbin/streamlinkSRV restart'
            self.session.openWithCallback(self.doNothing ,Console, title = mtitle, cmdlist = [ cmd ])
        
    def exit(self):
        self.VisibleSection = 0
        self.close(None)
        
    def prevConf(self):
        DBGlog('prevConf >>> VisibleSection = %s' % self.VisibleSection)
        self.VisibleSection -= 1
        if self.VisibleSection < 1:
            self.VisibleSection = 5
        self.refreshBuildList()
        
    def nextConf(self):
        DBGlog('nextConf >>> VisibleSection = %s' % self.VisibleSection)
        self.VisibleSection += 1
        if self.VisibleSection > 5:
            self.VisibleSection = 1
        self.refreshBuildList()
    
    def _isCDM(self):
        if config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value in ('?', 'L'):
            if not os.path.exists('/usr/lib/python3.12/site-packages/'):
                config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value = 'N'
            elif not os.path.exists('/usr/lib/python3.12/site-packages/emukodi/ExtPlayer/'):
                config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value = 'K'
            else:
                try:
                    from  pywidevine.cdmdevice.checkCDMvalidity import testDevice
                    retVal = testDevice()
                    if retVal is None: config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value = 'N'
                    elif retVal: config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value = 'Y'
                    else: config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value = 'L'
                    configfile.save()
                except Exception as e: 
                    DBGlog(str(e))
                    config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value = 'N'
                    configfile.save()
            config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.save()
            configfile.save()

    def layoutFinished(self):
        print('layoutFinished')
        self._isCDM()
        self.VisibleSection = 0
        self.DoBuildList.start(10, True)
        self.setTitle(self.setup_title)
        
        if os.path.exists("/usr/lib/enigma2/python/Plugins/SystemPlugins/ServiceApp/serviceapp.so"):
            self.choicesList = [(_("Don't change"),"0"),("gstreamer (root 4097)","4097"),("ServiceApp gstreamer (root 5001)","5001"), ("ServiceApp ffmpeg (root 5002)","5002"),("Hardware (root 1) wymagany do PIP","1")]
        else:
            self.choicesList = [(_("Don't change"),"0"),("gstreamer (root 4097)","4097"),("Hardware (root 1) wymagany do PIP","1"),(_("ServiceApp not installed!"), None)]
        
    def changedEntry(self):
        DBGlog('%s' % 'changedEntry()')
        try:
            for x in self.onChangedEntry:
                x()
        except Exception as e:
            DBGlog('%s' % str(e))

    def selectionChanged(self):
        if 0:
            DBGlog('%s' % 'selectionChanged(%s)' % self["config"].getCurrent()[0])

    def getCurrentEntry(self):
        return self["config"].getCurrent()[0]

    def getCurrentValue(self):
        if len(self["config"].getCurrent()) >= 2:
            return str(self["config"].getCurrent()[1].getText())

    def createSummary(self):
        return SetupSummary

    def Okbutton(self):
        DBGlog('%s' % 'Okbutton')
        try:
            self.doAction = None
            curIndex = self["config"].getCurrentIndex()
            selectedItem = self["config"].list[curIndex]
            if len(selectedItem) >= 2:
                currItem = selectedItem[1]
                currInfo = selectedItem[0]
                if isinstance(currItem, ConfigText):
                    from Screens.VirtualKeyBoard import VirtualKeyBoard
                    self.session.openWithCallback(self.OkbuttonTextChangedConfirmed, VirtualKeyBoard, title=(currInfo), text = currItem.value)
                elif currItem == config.plugins.streamlinkSRV.One:
                    if self.VisibleSection == 1: self.VisibleSection = 0
                    else: self.VisibleSection = 1
                    self.refreshBuildList()
                elif currItem == config.plugins.streamlinkSRV.Two:
                    if self.VisibleSection == 2: self.VisibleSection = 0
                    else: self.VisibleSection = 2
                    self.refreshBuildList()
                elif currItem == config.plugins.streamlinkSRV.Three:
                    if self.VisibleSection == 3: self.VisibleSection = 0
                    else: self.VisibleSection = 3
                    self.refreshBuildList()
                elif currItem == config.plugins.streamlinkSRV.Four:
                    if self.VisibleSection == 4: self.VisibleSection = 0
                    else: self.VisibleSection = 4
                    self.refreshBuildList()
                elif currItem == config.plugins.streamlinkSRV.Five:
                    if self.VisibleSection == 5: self.VisibleSection = 0
                    else: self.VisibleSection = 5
                    self.refreshBuildList()
                elif currItem == config.plugins.streamlinkSRV.WPbouquet:
                    if config.plugins.streamlinkSRV.WPusername.value == '' or config.plugins.streamlinkSRV.WPpassword.value == '':
                        self.session.openWithCallback(self.doNothing,MessageBox, _("Username & Password are required!"), MessageBox.TYPE_INFO, timeout = 5)
                        return
                    else:
                        self.doAction = ('wpBouquet.py' , '/etc/enigma2/userbouquet.WPPL.tv', config.plugins.streamlinkSRV.WPusername.value, config.plugins.streamlinkSRV.WPpassword.value)
                elif currItem == config.plugins.streamlinkSRV.WPlogin:
                    if config.plugins.streamlinkSRV.WPusername.value == '' or config.plugins.streamlinkSRV.WPpassword.value == '':
                        self.session.openWithCallback(self.doNothing,MessageBox, _("Username & Password are required!"), MessageBox.TYPE_INFO, timeout = 5)
                        return
                    else:
                        self.saveConfig()
                        cmd = "/usr/bin/python /usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/wpBouquet.py checkLogin '%s' '%s'" % (config.plugins.streamlinkSRV.WPusername.value, config.plugins.streamlinkSRV.WPpassword.value)
                        self.session.openWithCallback(self.doNothing ,Console, title = "SL %s %s" % (Version, _('Credentials verification')), cmdlist = [ cmd ])
                        return
                elif currItem == config.plugins.streamlinkSRV.generateBouquet:
                    DBGlog('currItem == config.plugins.streamlinkSRV.generateBouquet')
                    bouquetFileName = currInfo.split(': ')[1].strip()
                    self.doAction = ('generate_%s.py' % bouquetFileName, '/etc/enigma2/%s' % bouquetFileName, 'anonymous','nopassword')
                elif currItem == config.plugins.streamlinkSRV.removeBouquet: #removeBouquet
                    DBGlog('currItem == config.plugins.streamlinkSRV.removeBouquet')
                    #wybrany bukiet
                    bouquetFileName = currInfo.split(': ')[1].strip()
                    self.doAction = ('removeBouquet.py', '/etc/enigma2/%s' % bouquetFileName, _("Bouquet_'%s' _removed_properly") % bouquetFileName)
                elif currItem == config.plugins.streamlinkSRV.installBouquet: #installBouquet
                    DBGlog('currItem == config.plugins.streamlinkSRV.installBouquet')
                    #wybrany bukiet
                    bouquetFileName = currInfo.split(': ')[1].strip()
                    self.cleanBouquets_tvradio()
                    self.doAction = ('installBouquet.py', bouquetFileName)
                elif currItem == config.plugins.streamlinkSRV.downloadBouquet: #downloadBouquet
                    DBGlog('currItem == config.plugins.streamlinkSRV.installBouquet')
                    #wybrany bukiet
                    bouquetFileName = currInfo.split(': ',1)[1].split(' ',1)[0].strip()
                    self.cleanBouquets_tvradio()
                    url2bouquet = selectedItem[2]
                    #DBGlog('url2bouquet=%s' % url2bouquet)
                    self.doAction = ('downloadBouquet.py', bouquetFileName, url2bouquet, )
                elif currItem == config.plugins.streamlinkSRV.unmanagedBouquet: #modify local bouquet
                    DBGlog('currItem == config.plugins.streamlinkSRV.unmanagedBouquet')
                    #wybrany bukiet
                    bouquetFileName = currInfo.split(': ',1)[1].split(' ',1)[0].strip()
                    self.cleanBouquets_tvradio()
                    self.session.openWithCallback(self.localBouquetSelectedAction, ChoiceBox, title = _("What to do?"), list = [(_("Try to find correct reference to enable EPG"),"e"),
                                                                                                                                (_("Change framework"),"f"), 
                                                                                                                                (_("Change Streamlink connection type"),"sl")
                                                                                                                                ])
                    return
                elif currItem == config.plugins.streamlinkSRV.streamlinkEMUKODIconfig: #bouquets based on KODI plugins
                    DBGlog('currItem == config.plugins.streamlinkSRV.streamlinkEMUKODIconfig')
                    self.emuKodiActions(selectedItem)
                    return
                ####
                DBGlog('%s' % str(self.doAction))
                if not self.doAction is None:
                    cmd = self.doAction[0]
                    bfn = self.doAction[1]
                    DBGlog('%s' % bfn)
                    if cmd == 'removeBouquet.py':
                        cmd = '/usr/bin/python /usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/%s' % ' '.join(self.doAction)
                        self.session.openWithCallback(self.retFromCMD ,Console, title = "SL %s %s" % (Version, _('Removing bouquet...')), cmdlist = [ cmd ])
                    elif os.path.exists(bfn):
                        self.cmdTitle = _('Updating %s...') % bfn
                        self.session.openWithCallback(self.OkbuttonConfirmed, MessageBox, _("Do you want to update '%s' file?") % bfn, MessageBox.TYPE_YESNO, default = False)
                    elif cmd == 'downloadBouquet.py':
                        self.cmdTitle = _('Downloading %s...') % bfn
                        self.session.openWithCallback(self.OkbuttonConfirmed, MessageBox, _("Do you want to download '%s' file?") % bfn, MessageBox.TYPE_YESNO, default = False)
                    else:
                        self.cmdTitle = _('Creating %s...') % bfn
                        self.session.openWithCallback(self.OkbuttonConfirmed, MessageBox, _("Do you want to create '%s' file?") % bfn, MessageBox.TYPE_YESNO, default = True)
        except Exception as e:
            DBGlog('%s' % str(e))

    def localBouquetChangeFramework(self, ret ):
        if ret is None:
            DBGlog("localBouquetChangeFramework(ret ='%s')" % str(ret))
        else:
            self.doAction = self.doAction + ('f',)
            self.doAction = self.doAction + (ret[1],)
            self.session.openWithCallback(self.retFromCMD ,Console, title = "SL %s %s" % (Version, _('Modifying bouquet...')), cmdlist = [ ' '.join(self.doAction) ])

    def localBouquetChangeSLType(self, ret ):
        if ret is None:
            DBGlog("localBouquetchangeSLType(ret ='%s')" % str(ret))
        else:
            self.doAction = self.doAction + ('sl',)
            self.doAction = self.doAction + (ret[1],)
            self.session.openWithCallback(self.retFromCMD ,Console, title = "SL %s %s" % (Version, _('Modifying bouquet...')), cmdlist = [ ' '.join(self.doAction) ])

    def localBouquetSelectedAction(self, ret):
        curIndex = self["config"].getCurrentIndex()
        selectedItem = self["config"].list[curIndex]
        bouquetFileName = selectedItem[0].split(': ',1)[1].split(' ',1)[0].strip()
        
        self.doAction = ('/usr/bin/python', '/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/changeLocalBouquet.py', bouquetFileName, )
        
        if ret is None:
            DBGlog("localBouquetSelectedAction(ret ='%s')" % str(ret))
            return
        elif ret[1] == 'f': #Change framework
            self.session.openWithCallback(self.localBouquetChangeFramework, ChoiceBox, title = _("Select Multiframework"), list = self.choicesList)
        elif ret[1] == 'e': #Try to find correct reference to enable EPG
            self.doAction = self.doAction + ('e',)
            self.session.openWithCallback(self.retFromCMD ,Console, title = "SL %s %s" % (Version, _('Modifying bouquet...')), cmdlist = [ ' '.join(self.doAction) ])
            return
        elif ret[1] == 'sl': #Change Streamlink connection type
            self.session.openWithCallback(self.localBouquetChangeSLType, ChoiceBox, title = _("Select Streamlink connection type"), list = [(_("Use streamlinkSRV"),"SRV"), (_("Use Wrappers"),"wrapper"), 
                                                                                                                           (_("Use direct connection"),"direct")
                                                                                                                           ])
        
    def cleanBouquets_tvradio(self): #clean bouquets.tv from non existing files
        for TypBukietu in('/etc/enigma2/bouquets.tv','/etc/enigma2/bouquets.radio'):
            f = ''
            for line in open(TypBukietu,'r'):
                if 'FROM BOUQUET' in line:
                    fname = line.split('FROM BOUQUET')[1].strip().split('"')[1].strip()
                    if os.path.exists('/etc/enigma2/%s' % fname):
                        f += line
                else:
                    f += line
            open(TypBukietu,'w').write(f)
            
    def OkbuttonTextChangedConfirmed(self, ret ):
        if ret is None:
            DBGlog("OkbuttonTextChangedConfirmed(ret ='%s')" % str(ret))
        else:
            try:
                curIndex = self["config"].getCurrentIndex()
                self["config"].list[curIndex][1].value = ret
            except Exception as e:
                DBGlog('%s' % str(e))

    def OkbuttonConfirmed(self, ret = False):
        if ret:
            self.session.openWithCallback(self.SelectedFramework, ChoiceBox, title = _("Select Multiframework"), list = self.choicesList)

    def OkbuttonConfirmed2(self, ret = False):
        if ret:
            doActionPath = '/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/'
            cmd = '/usr/bin/python %s%s %s %s %s' % (doActionPath,
                                                 ' '.join(self.doAction),
                                                 config.plugins.streamlinkSRV.PortNumber.value,
                                                 '4097',
                                                 config.plugins.streamlinkSRV.useWrappers.value
                                                )
            DBGlog('%s' % cmd)
            self.session.openWithCallback(self.doNothing ,Console, title = "SL %s %s" % (Version, self.cmdTitle), cmdlist = [ cmd ])

    def SelectedFramework(self, ret):
        if not ret or ret == "None" or isinstance(ret, (int, float)):
            ret = (None,'4097')
        doActionPath = '/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/'
        cmd = '/usr/bin/python %s%s %s %s %s' % (doActionPath,
                                                 ' '.join(self.doAction),
                                                 config.plugins.streamlinkSRV.PortNumber.value,
                                                 ret[1],
                                                 config.plugins.streamlinkSRV.useWrappers.value
                                                )
        if self.doAction[0] == 'wpBouquet.py':
            DBGlog('%s WPuser WPpass %s %s' % (self.doAction[0], config.plugins.streamlinkSRV.PortNumber.value, ret[1]))
        else:
            DBGlog('%s' % cmd)
        self.session.openWithCallback(self.retFromCMD ,Console, title = "SL %s %s" % (Version, self.cmdTitle), cmdlist = [ cmd ])

    def reloadBouquets(self):
        from enigma import eDVBDB
        eDVBDB.getInstance().reloadBouquets()
        
    def retFromCMD(self, ret = False):
        DBGlog('retFromCMD >>>')
        self.cleanBouquets_tvradio()
        self.reloadBouquets()
        msg = _("Bouquets has been reloaded")
        self.session.openWithCallback(self.refreshBuildList,MessageBox, msg, MessageBox.TYPE_INFO, timeout = 5)

    def emuKodiConsoleCallback(self, ret = False):
        if self.emuKodiAction[1] == 'userbouquet': #akcja
            self.retFromCMD(ret)
    
    def emuKodiActionConfirmed(self, ret = False):
        from emukodi.e2Console import emukodiConsole
        self.emuKodiCmdsList = []
        if ret:
            dostawca = self.emuKodiAction[0]
            akcja = self.emuKodiAction[1]
            pythonRunner = '/usr/bin/python'
            #ustawienie skryptu uruchomienia
            if dostawca == 'playerpl':
                addonScript = 'plugin.video.playermb/main.py'
                runAddon = '%s %s' % (pythonRunner, os.path.join(addons_path, addonScript))
            #ustawienie parametrow w zaleznoci od akcji
            if akcja == 'LOGIN':
                autoClose = True
                if dostawca == 'playerpl':
                    self.emuKodiCmdsList.append(runAddon + " '1' '?mode=login' 'resume:false'") #ustawienie flagi logged, wymagane przez wtyczke
                    self.emuKodiCmdsList.append(runAddon + " '1' ' ' 'resume:false'")
            elif akcja == 'userbouquet':
                autoClose = False
                plikBukietu = '/etc/enigma2/userbouquet.%s.tv' % dostawca
                if dostawca == 'playerpl':
                    self.emuKodiCmdsList.append(runAddon + " '1' '?mode=listcategContent&url=%3alive' 'resume:false'")
                self.emuKodiCmdsList.append('%s %s %s "%s"' % (pythonRunner, os.path.join(emukodi_path, 'e2Bouquets.py'), plikBukietu, addonScript))
            
            #uruchomienie lancucha komend
            if len(self.emuKodiCmdsList):
                cleanWorkingDir()
                log("===== %s - %s ====" % (dostawca, akcja))
                self.session.openWithCallback(self.emuKodiConsoleCallback ,emukodiConsole, title = "SL %s %s-%s" % (Version, 'EmuKodi', dostawca), 
                                                cmdlist = self.emuKodiCmdsList, closeOnSuccess = autoClose)
            
    def emuKodiActions(self, selectedItem):
        DBGlog('emuKodiActions(%s)' % str(selectedItem))
        if len(selectedItem) < 3:
            self.session.openWithCallback(self.doNothing,MessageBox, 'Nie wiem co zrobić ;)', MessageBox.TYPE_INFO, timeout = 5)
            return
        else:
            self.emuKodiAction = selectedItem[2] #'playerpl', 'userbouquet'
            dostawca = self.emuKodiAction[0]
            akcja = self.emuKodiAction[1]
            if dostawca == 'playerpl' and akcja == 'LOGIN':
                MsgInfo = "Zostaniesz poproszony o podanie kodu w przeglądarce.\nBędziesz mieć na to maksimum 340 sekund i nie będziesz mógł przerwać.\n\nJesteś gotowy?"
                self.session.openWithCallback(self.emuKodiActionConfirmed, MessageBox, MsgInfo, MessageBox.TYPE_YESNO, default = False, timeout = 15)
                return
            elif dostawca == 'playerpl' and akcja == 'userbouquet':
                plikBukietu = '/etc/enigma2/userbouquet.%s.tv' % dostawca
                if os.path.exists(plikBukietu): MsgInfo = "Zaktualizować plik %s ?" % plikBukietu
                else: MsgInfo = "Utworzyć plik %s ?" % plikBukietu
                self.session.openWithCallback(self.emuKodiActionConfirmed, MessageBox, MsgInfo, MessageBox.TYPE_YESNO, default = False, timeout = 15)
                return
            else:
                self.doAction = ('emukodiBouquets.py', 'UNKNOWN', "'%s'" % selectedAction.replace(' ','_'))
                #DBGlog('currItem == config.plugins.streamlinkSRV.streamlinkEMUKODIconfig')
                #self.session.openWithCallback(self.doNothing ,Console, title = "SL %s %s" % (Version, _('Credentials verification')), cmdlist = [ cmd ])
        return
        #config.plugins.streamlinkSRV.IPTVdrmMoviePlayer.value
