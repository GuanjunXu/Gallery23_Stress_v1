#!/usr/bin/env python
from uiautomatorplug.android import device as d
import time
import unittest
import commands
import string
import util
import random

u = util.Util()
FLITER_LIST = ['Albums','Places','Events','Dates','People','Camera Roll','Media']

class GalleryTest(unittest.TestCase):

    def setUp(self):
        super(GalleryTest,self).setUp()
        #Add on May 26th due to device always reboot by itself
        if d(text = 'Charged').wait.exists(timeout = 2000):
            commands.getoutput('adb root')
            time.sleep(5)
            commands.getoutput('adb remount')
            d.swipe(530,1300,1000,1300)
        # clear test resource
        #self.util = util.Util
        u._clearAllResource()
        # push test pics.
        u._confirmResourceExists()
        # launch gallery
        u.launchGallery()


    def tearDown(self):
        super(GalleryTest,self).tearDown()
        #4.Exit activity
        u.pressBack(4)

    # Testcase 1
    def testSlideShowWithCine(self):
        """
        Summary: Slide Show with Cine mode
        Step:
        1. Launch SocialGallery app
        2. Enter grid view
        3. Tap Slideshow
        4. Select Cine Effect
        """
        # Step 2
        u.enterXView('gridview')
        for i in range(100):
            u.setMenuOptions('Slideshow')
            d(text = 'Cine Effect').click()
            time.sleep(3)
            # Since automation can't check this point, if it back to gridview treat it as pass.
            u.pressBack(1)
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)

    # Testcase 2
    def testSlideShowWithDissolve(self):
        """
        Summary: Slide Show with Dissolve mode
        Step:
        1. Launch SocialGallery app
        2. Enter grid view
        3. Tap Slideshow
        4. Select Dissolve Effect
        """
        # Step 2
        u.enterXView('gridview')
        for i in range(100):
            u.setMenuOptions('Slideshow')
            d(text = 'Dissolve').click()
            time.sleep(3)
            # Since automation can't check this point, if it back to gridview treat it as pass.
            u.pressBack(1)
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)

    # Testcase 3
    def testSlideShowWithFlash(self):
        """
        Summary: Slide Show with Flash mode
        Step:
        1. Launch SocialGallery app
        2. Enter grid view
        3. Tap Slideshow
        4. Select Flash Effect
        """
        # Step 2
        u.enterXView('gridview')
        for i in range (2):
            # Step 3 + Step 4
            u.setMenuOptions('Slideshow')
            d(text = 'Flash').click()
            time.sleep(3)
            # Since automation can't check this point, if it back to gridview treat it as pass.
            u.pressBack(1)
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)

    # Testcase 4
    def testSelectDeselectAll(self):
        """
        Summary: Select Deselect all
        Step:
        1. Launch gallery and open the folder in condition
        2. Long press a picture
        3. Tap on the drop down arrow and select "select all"
        4. Tap on the drop down arrow again and select "deselect all"
        """
        # Step 1
        u.enterXView('gridview')
        for i in range(100):
            # Step 2
            self._longtouchscreencenter()
            # Step 3
            d(text = '1 selected').click()
            d(text = 'Select all').click()
            # Step 4
            d(text = '20 selected').click()
            d(text = 'Deselect all').click()
            # Since automation can't check this point, if it back to gridview treat it as pass.
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)

    # Testcase 5
    def testLaunchGallery(self):
        """
        Summary: Slide Show with Flash mode
        Step:
        1. Launch gallery
        """
        u.pressBack(1)
        # Step 1
        for i in range(100):
            u.launchGallery()
            time.sleep(1)
            commands.getoutput('adb shell pm clear com.intel.android.gallery3d')

    # Testcase 6
    def testSwitchToCamera(self):
        """
        Summary: Launch camera from gallery
        Step:
        1. Launch gallery and tap on the camera icon at top right corner of screen
        2. Select social camera2.2
        """
        for i in range(100):
            #Step 1 + Step 2
            d(description = 'Switch to camera').click.wait()
            if  d(text = 'Complete action using').wait.exists(timeout = 2000):
                d(text = 'com.intel.camera22').click()
                d(text = 'Always').click.wait()
            # confirm camera launched
            if d(text = 'OK').wait.exists(timeout = 2000):
                d(text = 'OK').click.wait()
            if d(text = 'Cancel').wait.exists(timeout = 2000):
                d(text = 'Cancel').click.wait()
            time.sleep(3)
            assert d(description = 'Shutter button').wait.exists(timeout = 2000)
            u.pressBack(1)
            # confirm back to gallery
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)

    # Testcase 7
    def testSelectFliter(self):
        """
        Summary: Launch camera from gallery
        Step:
        1. Launch gallery 
        2. Tap on the drop down arrow and select location
        """
        for i in range(100):        
            fliter_list = random.choice(FLITER_LIST)
            u.selectFilter(fliter_list)
            assert d(text = fliter_list).wait.exists(timeout = 2000)

    def _longtouchscreencenter(self):
        d.swipe(550,1100,551,1101)
