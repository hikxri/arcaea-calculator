"""
Arcaea Calculator (and Score Manager, and B30 Generator)
made by sakura hikari

pycharm might give some warnings here and there but please ignore it
(unless you manage to fix it, then please let me know ♥)

feel free to use the source code however you wish, but please
mention / credit me if you publish it online
"""

import sys
import math
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QFont, QIntValidator, QFontMetrics
from func import *


class ImageWindow(QWidget):  # chatGPT wrote the basis of this code lol
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Top Entries')
        # self.setGeometry(500, 100, 600, 600)

        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.saveImage)

        layout = QVBoxLayout()
        layout.addWidget(self.save_button)
        layout.addWidget(self.label_image)
        self.setLayout(layout)

        self.painter = QPainter()
        self.full_size_pixmap = QPixmap()

    def generate_b30(self, song_data, background_file, username, censored=False):
        # initialization
        # set grid parameters
        num_cols = 5  # 6x5 grid
        num_rows = math.ceil(len(song_data) / 5)
        x_dist = 335
        y_dist = 272

        # set pixmap parameters
        width = 1800
        height = 460 + 272 * num_rows  # 2092 for b30
        pixmap = QPixmap(width, height)  # 900x1046 from arcaea's official b30 image
        pixmap.fill(QColor(19, 9, 33))

        self.painter = QPainter(pixmap)
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # text settings
        self.painter.setPen(QColor(255, 255, 255, 255))  # white
        font = QFont("Myriad")

        # draw
        # background
        # background image
        if not censored:
            self.drawBackgroundImage(background_file, width, height)

        # background rectangle
        bg_rect = QRect(75, 343, x_dist * (num_cols - 1) + 284 + 18, y_dist * (num_rows - 1) + 230 + 18)
        self.painter.fillRect(bg_rect, QColor(10, 10, 10, 150))

        # header
        font.setBold(True)
        font.setPointSize(70)
        self.painter.setFont(font)
        header_rect = QRect(0, 0, width, 300)
        self.drawTextWithOutLine(header_rect, Qt.AlignmentFlag.AlignCenter, f"Top {len(song_data)} Entries")
        font.setBold(False)

        # username
        if username:
            self.painter.setBrush(QColor(150, 150, 171, 200))
            font_width = QFontMetrics(font).horizontalAdvance(username)
            font_width = font_width // 2
            mid_point = (width // 2, 264)
            username_points = [
                QPoint(mid_point[0] - font_width, mid_point[1] + 40),
                QPoint(mid_point[0] - font_width - 40, mid_point[1]),
                QPoint(mid_point[0] - font_width, mid_point[1] - 40),
                QPoint(mid_point[0] + font_width, mid_point[1] - 40),
                QPoint(mid_point[0] + font_width + 40, mid_point[1]),
                QPoint(mid_point[0] + font_width, mid_point[1] + 40)
            ]
            self.painter.drawPolygon(username_points, Qt.FillRule.OddEvenFill)
            self.painter.setBrush(QColor(199, 199, 211, 200))

            font.setPointSize(50)
            self.painter.setFont(font)
            username_rect = QRect(0, 212, width, 100)
            self.drawTextWithOutLine(username_rect, Qt.AlignmentFlag.AlignCenter, f"{username}")

        # average play ptt
        font.setPointSize(30)
        self.painter.setFont(font)
        avg_rect = QRect(990, 210, 700, 50)
        self.drawTextWithOutLine(avg_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
                                 f"Average play potential: {getAveragePlayPotential(song_data):.3f}")

        # max play ptt
        max_rect = QRect(990, 255, 700, 50)
        if len(song_data) == 30:
            max_str = f"Max play potential: {getMaxPlayPotential(song_data):.3f}"
        else:
            max_str = f"Max play potential: -"
        self.drawTextWithOutLine(max_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, max_str)

        for i, song in enumerate(song_data):
            col = i % num_cols
            row = i // num_cols

            jacket_file = getSongJacket(song[0], song[1])

            # large rectangle
            if i <= 29:  # top 30th is at 29th index
                large_color = QColor(149, 131, 167, 200)
            else:
                large_color = QColor(110, 110, 110, 200)
            self.painter.fillRect(84 + x_dist * col, 352 + y_dist * row, 284, 230, large_color)

            # song index
            font.setPointSize(20)
            font.setBold(True)
            self.painter.setFont(font)
            if i <= 29:
                index_color = QColor(165, 122, 186, 255)
            else:
                index_color = QColor(130, 130, 130, 255)
            self.painter.fillRect(76 + x_dist * col, 364 + y_dist * row, 84, 48, index_color)
            index_rect = QRect(88 + x_dist * col, 372 + y_dist * row, 60, 40)
            self.painter.setPen(QColor(80, 80, 80, 200))  # black shadow
            self.painter.drawText(index_rect.translated(4, 4),
                                  Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, f"#{i + 1}")
            self.painter.setPen(QColor(255, 255, 255, 255))
            self.painter.drawText(index_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, f"#{i + 1}")
            font.setBold(False)

            # potential
            font.setPointSize(25)
            self.painter.setFont(font)
            potential = round(float(song[8]), 2)
            potential_rect = QRect(90 + x_dist * col, 415 + y_dist * row, 100, 40)
            self.drawTextWithOutLine(potential_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                                     f"{potential:.2f}")

            # chart constant
            font.setPointSize(20)
            self.painter.setFont(font)
            cc = song[3]
            cc_rect = QRect(92 + x_dist * col, 455 + y_dist * row, 100, 40)
            self.drawTextWithOutLine(cc_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, f"({cc})")

            # song jacket
            self.painter.fillRect(180 + x_dist * col, 362 + y_dist * row, 182, 182, QColor(41, 27, 57, 255))
            if not censored and jacket_file:
                jacket_pixmap = QPixmap(f"arcaea_song_files/{jacket_file}")\
                    .scaled(174, 174, transformMode=Qt.TransformationMode.SmoothTransformation)
                self.painter.drawPixmap(184 + x_dist * col, 366 + y_dist * row, jacket_pixmap)
            else:
                font = QFont("Comic Sans MS")
                font.setPointSize(20)
                self.painter.setFont(font)
                self.painter.setPen(QColor(0, 0, 0, 255))
                censored_rect = QRect(184 + x_dist * col, 366 + y_dist * row, 174, 174)
                self.painter.fillRect(censored_rect, QColor(255, 255, 255, 255))
                self.painter.drawText(censored_rect, Qt.AlignmentFlag.AlignCenter, song[0])
                self.painter.setPen(QColor(255, 255, 255, 255))
                font = QFont("Myriad")

            # song difficulty
            font.setPointSize(19)
            font.setBold(True)
            self.painter.setFont(font)
            if song[1] == "BYD":
                self.painter.setBrush(QColor(179, 87, 87, 255))
            if song[1] == "ETR":
                self.painter.setBrush(QColor(123, 96, 209, 255))
            if song[1] == "FTR":
                self.painter.setBrush(QColor(166, 83, 173, 255))
            if song[1] == "PRS":
                self.painter.setBrush(QColor(216, 211, 145, 255))
            if song[1] == "PST":
                self.painter.setBrush(QColor(73, 177, 215, 255))
            right_point = (334, 352)
            diamond_points = [
                QPoint(right_point[0] + x_dist * col, right_point[1] + y_dist * row),  # <
                QPoint(right_point[0] + 34 + x_dist * col, right_point[1] + 34 + y_dist * row),  # v
                QPoint(right_point[0] + 34 * 2 + x_dist * col, right_point[1] + y_dist * row),  # >
                QPoint(right_point[0] + 34 + x_dist * col, right_point[1] - 34 + y_dist * row)  # ^
            ]
            self.painter.drawPolygon(diamond_points, Qt.FillRule.OddEvenFill)
            difficulty_rect = QRect(right_point[0] + x_dist * col, right_point[1] - 36 + y_dist * row,
                                    34 * 2, 34 * 2)
            self.painter.setPen(QColor(80, 80, 80, 200))  # black shadow
            self.painter.drawText(difficulty_rect.translated(4, 4), Qt.AlignmentFlag.AlignCenter, song[2])
            self.painter.setPen(QColor(255, 255, 255, 255))
            self.painter.drawText(difficulty_rect, Qt.AlignmentFlag.AlignCenter, song[2])
            font.setBold(False)

            # score
            self.painter.fillRect(184 + x_dist * col, 516 + y_dist * row, 174, 24, QColor(41, 27, 57, 200))
            font.setPointSize(22)
            self.painter.setFont(font)
            score = stringToInt(song[4])
            score_rect = QRect(180 + x_dist * col, 506 + y_dist * row, 174, 40)
            self.drawTextWithOutLine(score_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
                                     f"{score:,}".replace(",", "'"))

            # grade
            self.painter.setBrush(QColor(199, 199, 211, 200))
            right_point = (95, 520)
            grade_points = [
                QPoint(right_point[0] + x_dist * col, right_point[1] + y_dist * row),  # <
                QPoint(right_point[0] + 23 + x_dist * col, right_point[1] + 23 + y_dist * row),  # v
                QPoint(right_point[0] + 23 + x_dist * col + 30, right_point[1] + 23 + y_dist * row),  # _
                QPoint(right_point[0] + 23 * 2 + x_dist * col + 30, right_point[1] + y_dist * row),  # >
                QPoint(right_point[0] + 23 + x_dist * col + 30, right_point[1] - 23 + y_dist * row),  # ^
                QPoint(right_point[0] + 23 + x_dist * col, right_point[1] - 23 + y_dist * row)  # -
            ]
            self.painter.drawPolygon(grade_points, Qt.FillRule.OddEvenFill)
            font.setPointSize(24)
            self.painter.setFont(font)
            grade_rect = QRect(right_point[0] + x_dist * col, right_point[1] - 23 + y_dist * row,
                               76, 40)
            grade = getGradeLevel(score)
            self.drawTextWithOutLine(grade_rect, Qt.AlignmentFlag.AlignCenter, grade,
                                     black=QColor(25, 25, 25, 255), color=QColor(201, 186, 230, 255))

            # song name
            font.setPointSize(20)
            self.painter.setFont(font)
            song_rect = QRect(92 + x_dist * col, 546 + y_dist * row, 270, 40)  # in case song name is too long
            song_name = song[0]
            self.drawTextWithOutLine(song_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, song_name)

        self.painter.end()

        self.full_size_pixmap = pixmap
        # return pixmap
        return pixmap.scaled(700, 700, Qt.AspectRatioMode.KeepAspectRatio,
                             transformMode=Qt.TransformationMode.SmoothTransformation)

    def drawBackgroundImage(self, background_file, width, height):
        bg_pixmap = QPixmap(f"backgrounds/{background_file}")
        w = bg_pixmap.rect().width()
        h = bg_pixmap.rect().height()
        if w / h < 1:  # portrait
            if height > h * width / w:
                bg_rect = QRect(-(int(w * height / h) - width) // 2, 0,
                                int(w * height / h), height)
            else:
                bg_rect = QRect(0, -(int(h * width / w) - height) // 2,
                                width, int(h * width / w))  # centered
        else:  # landscape
            if width > w * height / h:
                bg_rect = QRect(0, -(int(h * width / w) - height) // 2,
                                int(w * height / h), height)  # centered
            else:
                bg_rect = QRect(-(int(w * height / h) - width) // 2, 0,
                                int(w * height / h), height)  # centered

        self.painter.drawPixmap(bg_rect, blur_pixmap(bg_pixmap, 10))

    def drawTextWithOutLine(self, rect, alignment, text,
                            black=QColor(0, 0, 0, 200), color=QColor(255, 255, 255, 255)):
        self.painter.setPen(black)  # black outline
        for dx, dy in [(2, 2), (-2, 2), (2, -2), (-2, -2),
                       (2, 0), (-2, 0), (0, 2), (0, -2)]:
            self.painter.drawText(rect.translated(dx, dy), alignment, text)
        self.painter.setPen(color)  # real text
        self.painter.drawText(rect, alignment, text)

    def saveImage(self):
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("png")
        file_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png)")

        if file_path and self.full_size_pixmap:
            self.full_size_pixmap.save(file_path, "PNG")
            print("Image saved successfully.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # - initialize variables
        # -- csv file
        self.file_name = ""

        # -- set header, scores, from csv file
        self.header = []
        self.scores = []

        # -- initialize other variables
        self.DIFFICULTIES = ["PST", "PRS", "FTR", "ETR", "BYD"]
        self.selectedDifficulty = "FTR"
        self.selectedSong = "Testify"
        self.selectedScore = ""
        self.censored = False
        self.songList = []
        self.nonUnicodeSongList = []
        self.bgList = getBGList()
        self.selectedBg = "bg1.jpg"
        self.entriesCount = 30
        self.selectedUsername = loadUsername()
        # print(self.songList)

        # - window stuff
        self.setWindowTitle("Arcaea Calculator")

        # self.setStyleSheet("background-color: #434343;")

        layout = QGridLayout()

        # -- set buttons
        self.fileButton = QPushButton("Select file")
        self.fileButton.clicked.connect(self.setFile)

        self.fileLabel = QLabel()
        self.fileLabel.setWordWrap(True)

        self.songDropdown = QComboBox()
        self.songDropdown.addItems(self.nonUnicodeSongList)
        self.songDropdown.currentTextChanged.connect(self.setSong)
        self.songDropdown.setEditable(True)
        self.songDropdown.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.songDropdown.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.songDropdown.completer().setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # self.songDropdown.completer().highlighted.connect(self.autoCompleteSong)

        self.difficultyButtons = []
        for index, value in enumerate(self.DIFFICULTIES):
            difficulty_button = QPushButton(value)
            difficulty_button.setCheckable(True)
            difficulty_button.toggled.connect(lambda state, i=index: self.setDifficulty(i, state))  # ???
            self.difficultyButtons.append(difficulty_button)

        self.scoreField = QLineEdit()
        self.scoreField.setMaxLength(8)  # max score is 10'00X'XXX
        self.scoreField.setPlaceholderText("Enter score here... (No spaces or commas)")
        self.scoreField.textEdited.connect(self.setScore)
        self.scoreValidator = QIntValidator(0, 20_000_000)
        self.scoreField.setValidator(self.scoreValidator)

        self.addButton = QPushButton("Add score")
        self.addButton.clicked.connect(self.addScore)

        self.b30Button = QPushButton("Top 30 Entries")
        self.b30Button.clicked.connect(self.showB30)

        self.b30Censored = QPushButton("Censored")
        self.b30Censored.setCheckable(True)
        self.b30Censored.toggled.connect(self.setCensored)

        self.bgDropdown = QComboBox()
        self.bgDropdown.addItems(self.bgList)
        self.bgDropdown.currentTextChanged.connect(self.setBgFile)

        self.entriesField = QLineEdit()
        self.entriesField.setMaxLength(3)
        self.entriesField.setPlaceholderText("Number of Scores")
        self.entriesField.textEdited.connect(self.setEntriesCount)
        self.entriesValidator = QIntValidator(1, 100)
        self.entriesField.setValidator(self.entriesValidator)

        self.usernameField = QLineEdit()
        self.usernameField.setPlaceholderText("Enter username here...")
        self.usernameField.setText(self.selectedUsername)
        self.usernameField.textEdited.connect(self.setUsername)

        self.resultLabel = QLabel("")

        # -- initialize button states
        self.setFile(start=True)
        self.setSong(self.selectedSong)
        self.difficultyButtons[2].setChecked(True)  # initial difficulty is FTR

        # -- add widgets to layout
        layout.addWidget(self.fileButton,           0, 0, 1, 2)
        layout.addWidget(self.fileLabel,            0, 2, 1, 3)
        layout.addWidget(self.songDropdown,         1, 0, 1, 5)
        for index, button in enumerate(self.difficultyButtons):
            layout.addWidget(button, 2, index)
        layout.addWidget(self.scoreField,           3, 0, 1, 5)
        layout.addWidget(self.addButton,            4, 0, 1, 3)
        layout.addWidget(self.b30Button,            4, 3, 1, 2)
        layout.addWidget(self.b30Censored,          5, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.bgDropdown,           5, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.entriesField,         6, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.usernameField,        7, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.resultLabel,          5, 0, 5, 3, alignment=Qt.AlignmentFlag.AlignTop)

        # -- add layout to window
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.imageWindow = ImageWindow()

    # these functions are not ordered at all lmao, i just add them as i go on
    def setUsername(self, s):
        self.selectedUsername = s
        saveUsername(s)

    def setEntriesCount(self, s):
        if s == "":
            self.entriesCount = 30
            self.b30Button.setText("Top 30 Entries")
        else:
            self.b30Button.setText(f"Top {s} Entries")
            self.entriesCount = int(s)

    def setBgFile(self, s):
        self.selectedBg = s

    def setCensored(self, checked):
        if checked:
            self.censored = True
            self.bgDropdown.setEnabled(False)
        else:
            self.censored = False
            self.bgDropdown.setEnabled(True)

    def setFile(self, start=False):  # start: at start-up
        if start:
            file_name, header, scores = loadFile(start=True)
        else:
            file_name, header, scores = loadFile(start=False)

        if header == ['Title', 'Difficulty', 'Level', 'Chart Constant', 'Score',
                      'Note Count', 'PM Rating', 'Play Rating', 'Play Potential']:
            self.file_name = file_name
            self.header = header
            self.scores = scores
            self.fileLabel.setText(file_name)
            self.songList = getSongList(self.scores)
            self.nonUnicodeSongList = unicodeToTextArray(self.songList)
            self.songDropdown.clear()
            self.songDropdown.addItems(self.nonUnicodeSongList)
            saveFileName(self.file_name)

        else:
            if not start:
                self.fileLabel.setText("Invalid file!")

    def showB30(self):
        # b30 = getB30(self.scores)
        top_entries = getTopEntries(self.scores, self.entriesCount)

        image_pixmap = self.imageWindow.generate_b30(top_entries, self.selectedBg,
                                                     self.selectedUsername, censored=self.censored)

        self.imageWindow.label_image.setPixmap(image_pixmap)
        self.imageWindow.show()

    def addScore(self):
        question_box = QMessageBox()
        question_box.setIcon(QMessageBox.Icon.Question)
        choice = question_box.question(self, "?", "Are you sure?",
                                       QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if choice == QMessageBox.StandardButton.Yes:
            try:
                self.calculatePTT()  # if error occurs then it won't write
                index = getSongIndex(self.scores, self.selectedSong, self.selectedDifficulty)
                # new score must be greater than old score
                # print(stringToInt(self.scores[index][4]))
                if int(self.selectedScore) > stringToInt(self.scores[index][4]):
                    self.writeNewScore(index, int(self.selectedScore))
                    self.resultLabel.setText("Score added!")
                else:
                    self.resultLabel.setText("Score is not added!"
                                             "\nScore is less than or equal to old score.")

            except Exception as e:
                error_box = QMessageBox()
                error_box.setIcon(QMessageBox.Icon.Critical)
                error_box.setText("Oh no! An error occurred!")
                print(e)

    def calculatePTT(self):
        if not self.selectedScore:
            return None
        try:
            song_index = getSongIndex(self.scores, self.selectedSong, self.selectedDifficulty)
            cc = float(self.scores[song_index][3])

            score = int(self.selectedScore)
            play_rating = getPlayRating(score)
            play_ptt = getPlayPotential(cc, play_rating)

            return [song_index, cc, score, play_rating, play_ptt]

        except Exception as e:  # "too broad exception clause" i don't give a FUCK, pycharm
            print(e)
            return None

    def showCalculation(self):
        calc = self.calculatePTT()
        if calc:
            score_diff = calc[2] - stringToInt(self.scores[calc[0]][4])
            if score_diff > 0:
                score_diff_str = "+" + f"{score_diff:08,}".replace(",", "'")
            elif score_diff < 0:
                score_diff = -score_diff
                score_diff_str = "-" + f"{score_diff:08,}".replace(",", "'")
            else:
                score_diff_str = "0"
            self.resultLabel.setText(f"Song: {self.selectedSong}\n"
                                     f"Chart constant: {calc[1]} ({self.scores[calc[0]][2]})\n"
                                     f"Score: {calc[2]:,}".replace(",", "'") + f" ({score_diff_str})\n"
                                     f"Play rating: {round(calc[3], 3)} ({round(calc[3], 6)})\n"
                                     f"Play potential: {round(calc[4], 3)} ({round(calc[4], 6)})\n")

    def setDifficulty(self, index, checked):
        # uncheck other difficulty select buttons
        if checked:
            for i, button in enumerate(self.difficultyButtons):
                if i != index:
                    button.setChecked(False)

            # set difficulty
            self.selectedDifficulty = self.DIFFICULTIES[index]
            # print(self.selectedDifficulty)

        if self.selectedScore:
            self.showCalculation()

    def setSong(self, s):
        # only autocomplete when typing, not deleting
        if len(s) - len(self.selectedSong) == 1:
            # if has only one completion, make the completion the text
            if self.songDropdown.completer().completionCount() == 1:
                s = self.songDropdown.completer().currentCompletion()
                self.songDropdown.setEditText(s)
                self.selectedSong = s

        self.selectedSong = unicodeToText(s, inverse=True)
        # print(self.selectedSong)

        for index, button in enumerate(self.difficultyButtons):
            if index in filterDifficultyBySong(self.scores, self.selectedSong):
                button.setEnabled(True)
            else:
                button.setEnabled(False)

        if self.selectedScore and self.selectedSong in self.songList:
            self.showCalculation()

    def setScore(self, s):
        self.selectedScore = s
        # print(self.selectedScore)

        self.showCalculation()

    def writeNewScore(self, index, score):
        play_rating = getPlayRating(score)
        cc = float(self.scores[index][3])

        if play_rating == 2.0:
            pm_rating = score - 10_000_000 - stringToInt(self.scores[index][5])
            if pm_rating == 0:
                self.scores[index][6] = "MAX"
            else:
                self.scores[index][6] = pm_rating

        self.scores[index][4] = score
        self.scores[index][7] = play_rating
        self.scores[index][8] = getPlayPotential(cc, play_rating)

        # writing csv file
        with open(self.file_name, mode='w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.header)
            writer.writerows(self.scores)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
