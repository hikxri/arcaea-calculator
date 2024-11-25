import json
import os
import csv
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor


def listDir(path):
    return os.listdir(os.path.join(os.path.dirname(__file__), path))

def openJson(path, mode, encoding):
    return open(os.path.join(os.path.dirname(__file__), path), mode=mode, encoding=encoding)


def getPotentialColor(potential):
    try:
        potential = float(potential)

        if potential >= 13.00:
            return 207, 67, 118
        elif potential >= 12.50:
            return 174, 17, 96
        elif potential >= 12.00:
            return 207, 103, 122
        elif potential >= 11.00:
            return 169, 18, 46
        elif potential >= 10.00:
            return 166, 83, 173
        elif potential >= 7.00:
            return 124, 55, 135
        elif potential >= 3.50:
            return 73, 177, 215
        else:
            return 63, 137, 148

    except Exception as e:
        print(e)
        return 121, 121, 121


def saveUsername(username):
    json_file = openJson("save_data.json", mode='r', encoding='utf-8')
    save_dict = json.load(json_file)
    save_dict["username"] = username
    json_file.close()

    json_file = openJson("save_data.json", mode='w', encoding='utf-8')
    json.dump(save_dict, json_file)
    json_file.close()


def loadUsername():
    json_file = openJson("save_data.json", mode='r', encoding='utf-8')
    save_dict = json.load(json_file)
    json_file.close()
    return save_dict["username"]


def loadFile(start=False):
    if not start:
        file_name, _ = QFileDialog.getOpenFileName(caption="Open file", filter="CSV Files (*.csv)")
    else:
        file_name = loadFileName()
    if not file_name:
        return '', '', ''
    if not os.path.isfile(file_name):
        saveFileName("")
        return '', '', ''
    file = open(file_name, mode='r', encoding='utf-8')
    reader = csv.reader(file)

    header = next(reader)
    scores = [item for item in reader if len(item) > 0]

    file.close()
    return file_name, header, scores


def saveFileName(file_name):
    json_file = openJson("save_data.json", mode='r', encoding='utf-8')
    save_dict = json.load(json_file)
    save_dict["file_name"] = file_name
    json_file.close()

    json_file = openJson("save_data.json", mode='w', encoding='utf-8')
    json.dump(save_dict, json_file)
    json_file.close()


def loadFileName():
    json_file = openJson("save_data.json", mode='r', encoding='utf-8')
    save_dict = json.load(json_file)
    json_file.close()
    return save_dict["file_name"]


def unicodeToTextArray(array, inverse=False):
    json_file = openJson("nonunicode.json", mode='r', encoding='utf-8')
    song_dict = json.load(json_file)
    result = []

    if not inverse:  # unicode -> text
        for song_name in array:
            if song_name in song_dict:
                result.append(song_dict[song_name])
            else:
                result.append(song_name)

    else:
        song_dict_inv = {v: k for k, v in song_dict.items()}
        for song_name in array:
            if song_name in song_dict_inv:
                result.append(song_dict[song_name])
            else:
                result.append(song_name)

    json_file.close()
    return result


def unicodeToText(string, inverse=False):
    json_file = openJson("nonunicode.json", mode='r', encoding='utf-8')
    song_dict = json.load(json_file)
    if not inverse:
        if string in song_dict:
            json_file.close()
            return song_dict[string]
        json_file.close()
        return string

    else:
        song_dict_inv = {v: k for k, v in song_dict.items()}
        if string in song_dict_inv:
            json_file.close()
            return song_dict_inv[string]
        json_file.close()
        return string


def stringToInt(string):
    # for scores, note counts with commas, i.e., 10,002,221
    if type(string) is str:
        return int(string.replace(',', '').replace("'", ''))
    else:  # if it is already an int
        return string


def getPlayRating(score):
    if score >= 10_000_000:
        return 2.0
    elif score > 9_800_000:
        return 1 + (score - 9_800_000)/200_000
    else:
        return (score - 9_500_000)/300_000


def getPlayPotential(cc, score_modifier):
    return max(cc + score_modifier, 0)


# for old code
def getB30(score_list):
    score_list.sort(key=lambda x: float(x[8]), reverse=True)
    return score_list[:30]


def getTopEntries(score_list, entries_count):
    score_list.sort(key=lambda x: float(x[8]), reverse=True)
    return score_list[:entries_count]


def getAveragePlayPotential(top_entries):
    play_potentials = [float(item[8]) for item in top_entries]
    return sum(play_potentials) / len(top_entries)


def getMaxPlayPotential(top_entries):
    play_potentials = [float(item[8]) for item in top_entries]
    return (sum(play_potentials) + sum(play_potentials[:10])) / 40


def getGradeLevel(score):
    score = stringToInt(score)
    if score >= 10_000_000:
        return "PM"
    elif score >= 9_900_000:
        return "EX+"
    elif score >= 9_800_000:
        return "EX"
    elif score >= 9_500_000:
        return "AA"
    elif score >= 9_200_000:
        return "A"
    elif score >= 8_900_000:
        return "B"
    elif score >= 8_600_000:
        return "C"
    else:
        return "D"


def getSongList(score_list):
    result = []
    for item in score_list:
        if item[0] not in result:
            result.append(item[0])
    return result


# i don't think this function is needed
def groupSongsByDifficulty(score_list):
    sort_order = {"BYD": 0,
                  "ETR": 1,
                  "FTR": 2,
                  "PRS": 3,
                  "PST": 4}
    score_list.sort(key=lambda x: sort_order[x[1]])
    return score_list


# not needed anymore
def filterSongsByDifficulty(score_list, difficulty="", level=""):
    result = []

    # this code sucks but i won't change it
    if difficulty and level:
        for item in score_list:
            if item[1] == difficulty and item[2] == level:
                result.append(item[0])
    elif difficulty:
        for item in score_list:
            if item[1] == difficulty:
                result.append(item[0])
    elif level:
        for item in score_list:
            if item[2] == level:
                result.append(item[0])

    return result


def filterDifficultyBySong(score_list, song_name):
    result = []
    diff_dict = {"PST": 0,
                 "PRS": 1,
                 "FTR": 2,
                 "ETR": 3,
                 "BYD": 4}
    for song in score_list:
        if song[0] == song_name:
            result.append(song[1])

    return [diff_dict.get(item) for item in result]


def getSongIndex(score_list, song_name, difficulty):
    for index, item in enumerate(score_list):
        if item[0] == song_name and item[1] == difficulty:
            return index
    return -1


def getSongJacket(song_name, difficulty):
    song_name = unicodeToText(song_name).lower().replace(" ", "_")
    replace_list = ["!", "*", "#", "[", "]", "?", ":", ",", "|"]  # i manually renamed and checked every file
    for i in replace_list:
        song_name = song_name.replace(i, "")

    all_files = listDir("arcaea_song_files/")  # list of all song jackets

    if song_name + "_" + difficulty.lower() + ".jpg" in all_files:
        return song_name + "_" + difficulty.lower() + ".jpg"
    if song_name + ".jpg" in all_files:
        return song_name + ".jpg"
    return None


def getBGList():
    return listDir("backgrounds")
    # return os.listdir("/backgrounds/")


def blur_pixmap(pixmap, radius):
    scene = QGraphicsScene()
    pixmap_item = QGraphicsPixmapItem(pixmap)
    pixmap_item.setGraphicsEffect(QGraphicsBlurEffect(blurRadius=radius))
    scene.addItem(pixmap_item)

    # Create a blank QImage to render the QGraphicsScene onto
    image = QImage(pixmap.size(), QImage.Format.Format_ARGB32)
    image.fill(QColor("transparent"))

    painter = QPainter(image)
    scene.render(painter)
    painter.end()

    return QPixmap.fromImage(image)
