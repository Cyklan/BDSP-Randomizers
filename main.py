from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

from Randomizers import Encounters, Evolutions, Trainers, UndergroundEncounters, Levels, Shop, TM, Starters, TMCompat, Ability, FldItems, Moves
from Randomizers.dialog import Ui_MainWindow
from AdditionalMods import truesize, weatherRemove, hgssWalkSpeed
from Utilities import GlobalGameManager
import AtmospherePaths

from os import error, path, remove, getcwd, chdir, mkdir
from math import isclose
import shutil
import sys
import traceback
import subprocess
import configparser

class AppWindow(QMainWindow):
    
    atmospherePath = "atmosphereRandomized"
    emulatorPath = "emulatorRandomized"
    pathList = (atmospherePath, emulatorPath)
    romfs_bd = ""
    romfs_sp = ""

    save_bd = ""
    save_sp = ""

    mods_bd = ""
    mods_sp = ""
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnRandomize.clicked.connect(self.buttonClicked)

        config = configparser.ConfigParser()
        config.read("rando.ini")
        
        self.romfs_bd = config["ROMFS"]["brilliant_diamond"]
        self.romfs_sp = config["ROMFS"]["shining_pearl"]

        self.save_bd = config["SAVE_DIRS"]["brilliant_diamond"]
        self.save_sp = config["SAVE_DIRS"]["shining_pearl"]

        self.mods_bd = config["MOD_DIRS"]["brilliant_diamond"]
        self.mods_sp = config["MOD_DIRS"]["shining_pearl"]

    def randomize(self, game):
        global romFSPath

        if path.exists(path.join(romFSPath, "Data")):
            romFSPath = path.join(romFSPath, "Data")
            
        self.ui.tbLog.append("RomFS Directory set to " + romFSPath)
        
        self.ui.tbLog.append("Output folder set to {}".format(path.join(getcwd(), "mods")))
        
        cwd = getcwd()
        
        #Deletes remnamts of old randomizer
        if path.exists("mods"):
            shutil.rmtree("mods")
            
        chdir(cwd)
        
        try:
            
            if self.ui.cbStarters.isChecked():
                Starters.RandomizeStarters(self.ui.tbLog, romFSPath)
        
            if self.ui.cbPokemon.isChecked():
                self.ui.tbLog.append('Randomizing Pokemon!')
                generations = []
                if self.ui.cbGen1.isChecked():
                    generations.append(1)
                if self.ui.cbGen2.isChecked():
                    generations.append(2)
                if self.ui.cbGen3.isChecked():
                    generations.append(3)
                if self.ui.cbGen4.isChecked():
                    generations.append(4)
                #Fixed added safari -- sangawku
                Encounters.RandomizeEncounters(self.ui.tbLog,self.ui.cbLegends.isChecked(), generations, self.ui.cbSafari.isChecked(), romFSPath)
                
            if self.ui.cbEncounterLevel.isChecked() and not isclose(self.ui.sbEncounterLevel.value(), 0.0):
                self.ui.tbLog.append("Increasing Wild Encounter Levels!")
                levelIncrease = self.ui.sbEncounterLevel.value() / 100.0
                Encounters.LevelIncrease(self.ui.tbLog, levelIncrease, romFSPath)
                
            if self.ui.cbMoves.isChecked():
                self.ui.tbLog.append('Randomizing Movesets!')
                Moves.RandomizerMoves(self.ui.tbLog, romFSPath)
                self.ui.tbLog.append('Updating Trainer Movesets!')
                Trainers.updateMovesets(self.ui.tbLog, romFSPath)
                
            if self.ui.cbTrainers.isChecked():
                self.ui.tbLog.append('Randomizing Trainers!')
                Trainers.RandomizeTrainers(self.ui.tbLog, 0, 0, romFSPath, scaleWithLevel=False)
                
            if self.ui.cbTrainerLevel.isChecked() and not isclose(self.ui.sbTrainerLevel.value(), 0.0):
                levelIncrease = self.ui.sbTrainerLevel.value() / 100.0
                Trainers.LevelIncrease(self.ui.tbLog, levelIncrease, romFSPath)
                
            if self.ui.cbTimeSkip.isChecked() or self.ui.cb60FPS.isChecked():
                self.ui.tbLog.append('Applying Utilities!')
                GlobalGameManager.ApplyUtilities(self.ui.cb60FPS.isChecked(), self.ui.sbTimeStep.value(), self.ui.tbLog, romFSPath)
            
            if self.ui.cbUnderground.isChecked():
                self.ui.tbLog.append('Randomizing Underground Pokemon!')
                UndergroundEncounters.RandomizeUG(self.ui.tbLog, romFSPath)
                
            if self.ui.cbEvolutions.isChecked():
                self.ui.tbLog.append('Randomizing Evolutions!')
                Evolutions.RandomizeEvolutions(self.ui.tbLog, romFSPath)
            
            if self.ui.cbTM.isChecked():
                self.ui.tbLog.append('Randomizing TMs!')
                TM.RandomizeTMs(self.ui.tbLog, romFSPath)
            
            if self.ui.cbShops.isChecked():
                self.ui.tbLog.append('Randomizing Shops!')
                Shop.RandomizeShops(self.ui.tbLog, romFSPath)
            
            if self.ui.cbTMCompat.isChecked():
                TMCompat.RandomizeCompat(self.ui.tbLog, romFSPath)
            
            if self.ui.cbAbilities.isChecked():
                Ability.RandomizeAbilities(self.ui.tbLog, romFSPath)
            
            if self.ui.cbFieldItems.isChecked():
                FldItems.RandomizeFieldItems(self.ui.tbLog, romFSPath)
            
            
            ##------------------------------ Mods Section ------------------------------------    
            if self.ui.cbTrueSize.isChecked():
                truesize.truesize(self.ui.tbLog, romFSPath)
                
            if self.ui.cbRemoveWeather.isChecked():
                weatherRemove.removeWeather(self.ui.tbLog, romFSPath)
                
            if self.ui.cbFollowing.isChecked():
                hgssWalkSpeed.HGSSfollowing(self.ui.tbLog, romFSPath)
                
            ##Deletes temp files at the end
            moves = "Resources//tempMoveIndex.txt"
            
            tempFileList = [moves]
            for file in tempFileList:
                if path.exists(file):
                    remove(file)
                    
            if path.exists("mods"):
                if game == "bd":
                    # todo: copy dirs in mods into self.modsBD
                    self.write_mods(self.mods_bd)
                elif game == "sp":
                    self.write_mods(self.mods_sp)
                
            chdir(cwd)
                
        except Exception: 
            self.ui.tbLog.append("An Error has occured: ")
            self.ui.tbLog.append(traceback.format_exc())
            chdir(cwd)
            # self.ui.tbLog.append(str(type(inst.args)))
        #if self.ui.cbLevels.isChecked():
        #    self.ui.tbLog.append('Randomizing Levels!')
        #    if self.ui.rbFlat.isChecked():
        #        Levels.RandomizeLevels(self.ui.tbLog,1, self.ui.sbMin.value(), self.ui.sbMax.value())
        #    else:
        #        Levels.RandomizeLevels(self.ui.tbLog,0, self.ui.sbMin.value(), self.ui.sbMax.value())

    def write_mods(self, mod_path):
        cwd = getcwd()
        romfs_mod_path = path.join(cwd, "mods/emulatorRandomized", "romfs")
        exefs_mod_path = path.join(cwd, "mods/emulatorRandomized", "exefs")

        starters_mod_path = path.join(mod_path, "Starters")
        randomizer_mod_path = path.join(mod_path, "Randomizer")

        if path.exists(starters_mod_path):
            shutil.rmtree(starters_mod_path)
        
        if path.exists(randomizer_mod_path):
            shutil.rmtree(randomizer_mod_path)
        
        mkdir(starters_mod_path)
        mkdir(randomizer_mod_path)

        shutil.copytree(romfs_mod_path, path.join(randomizer_mod_path, "romfs"))
        shutil.copytree(exefs_mod_path, path.join(starters_mod_path, "exefs"))

    def write_save_games(self):
        self.ui.tbLog.append('Resetting Saves!')
        cwd = getcwd()
        shutil.rmtree(self.save_bd)
        shutil.rmtree(self.save_sp)
        shutil.copytree(path.join(cwd, "saves", "bd"), self.save_bd)
        shutil.copytree(path.join(cwd, "saves", "sp"), self.save_sp)

    
    def buttonClicked(self):
        #setup directory where romFS Tok modify is. 
        self.ui.tbLog.append('Starting...\n')
        global romFSPath
        romFSPath = self.romfs_bd
        self.randomize("bd")

        romFSPath = self.romfs_sp
        self.randomize("sp")

        self.write_save_games()
        self.ui.tbLog.append('All done!')
        

        

app = QApplication(sys.argv)

# Set our style, We don't want mismatched themes 
app.setStyle("Fusion")

# Now make them bitches dark as night:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)
app.setApplicationName("BDSP Randomizer")

w = AppWindow()
w.show()
sys.exit(app.exec_())

w = AppWindow()
w.show()
app.exec_()

