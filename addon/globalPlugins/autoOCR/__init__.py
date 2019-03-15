# coding=utf-8
#Copyright (C) 2019 autoOCR <larry.wang.801@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""autoOCR:
A global plugin that does auto OCR
"""
from __future__ import unicode_literals
import addonHandler
import globalPluginHandler
from contentRecog import RecogImageInfo
from scriptHandler import script
from logHandler import log
import ui
import globalVars
import config
_ = lambda x: x
# We need to initialize translation and localization support:
addonHandler.initTranslation()
category_name = _(u"Auto OCR")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def event_becomeNavigatorObject(self, obj, nextHandler, isFocus=False):
        if self.autoOCREnabled:
            from contentRecog import recogUi, uwpOcr
            recogUi.recognizeNavigatorObject(uwpOcr.UwpOcr())
        nextHandler()
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        if globalVars.appArgs.secure:
            return
        if config.isAppX:
            return
        self.autoOCREnabled = False
    # Translators: OCR command name in input gestures dialog
    @script(description=_("Toggle auto ocr"),
            category=category_name, gestures=["kb:control+;"])
    def script_toggleAutoOCR(self, gesture):
        import winVersion
        import ui
        if not winVersion.isUwpOcrAvailable():
            # Translators: Reported when Windows 10 OCR is not available.
            ui.message(_("Windows 10 OCR not available"))
            return
        if self.autoOCREnabled:
            self.autoOCREnabled = False
            # Translators: Reported when auto OCR is disabled
            ui.message(_(u"Auto OCR Disabled"))
        else:
            self.autoOCREnabled = True
            # Translators: Reported when auto OCR is enabled
            ui.message(_(u"Auto OCR Enabled"))