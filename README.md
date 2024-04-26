# Arcaea Score Manager and B30 Generator

A simple UI to input your Arcaea scores and generate your top entries as an image file. This application is based
on [Arcaea B30 Calculator (community)](https://docs.google.com/spreadsheets/d/1RJkupRtpRxxrTrMpb0VwCLZzOU0JtX_jsuo8xUnEO1k/edit?usp=sharing)
by [u/Chibu68_](https://www.reddit.com/user/Chibu68_/) and [u/hokandor7](https://www.reddit.com/user/hokandor7/).

The [scores.csv](scores.csv) blank template is updated as per `Arcaea v5.6.0`.

For users, I recommend reading [**Installation: For Users**](#for-users) and [**Usage**](#usage)
to help you get started!

**IMPORTANT: Your scores file must be in Comma Separated Values (.csv) file extension.** The header of the file should
be:
```Title,Difficulty,Level,Chart Constant,Score,Note Count,PM Rating,Play Rating,Play Potential```
.

I recommend making a backup of the .csv file in case the application goes bonkers.

## Installation

### For Users

If you simply want to use the application without making any significant changes to the source code, follow these steps.

1. Download the `Arcaea-Calculator.zip` file from
   the [releases](https://github.com/hikxri/arcaea-calculator/releases/latest) page.
2. Extract the ZIP contents to a location of your choice.
3. Run the executable file `Arcaea Calculator.exe`
   from there.

#### For Outdated Data

If the files from the [releases](https://github.com/hikxri/arcaea-calculator/releases/latest) page is
outdated:

1. Download the [scores.csv](scores.csv), [nonunicode.json](nonunicode.json), and `arcaea_song_files` files from
   the repository.
2. Replace the outdated files with the downloaded files.

### For Contributors

If you're interested in contributing or making modifications to the source code, follow these steps:

1. Clone the repository.
2. Install dependencies: `pip install PyQt6`
3. Run the application: `python main.py`

Now you can make improvements to the source code!

## Usage

1. **Launch the application.** A UI will pop up.
2. **Click the `Select file` button** and **import your Arcaea scores** as a `.csv` file.
    - Note that your scores file does not have to be in the same directory as the application.
3. After this:
    - **Using the score manager**:
        - **Enter the song name** in the first line edit box. The difficulty buttons should be enabled / disabled
          relative to the song selected.
        - **Select the difficulty** of the song.
        - **Type in the score** in the second line edit box.
        - **Click `Add score`** to save the score to your `.csv` file.
    - **Generating top entries**:
        - (Optional) **(For Arcaea Discord users)** Since Arcaea's official Discord disallows sending song jackets and
          World Mode backgrounds (it breaks their "data-mining" rule), **click the `Censored` button.** It will hide
          all "data-mined" features from the result image.
        - (Optional) **Select the background image** from the dropdown.
        - (Optional) **Enter the number of scores to be shown** in the result image. **Leave blank for 30 scores**,
          a.k.a. B30.
        - (Optional) **Enter the username to be shown** in the result image. The username is saved and will be
          automatically inputted upon launching the application again.
        - (Optional) **Enter the potential to be shown** in the result image. It will be shown on the left of the
          username. If there exists no username, it will be shown in the middle, below the title.
        - **Click the `Top 30 Entries`** (or`Top n entries`) **button**. A new window will pop up with a scaled-down
          version of the result image.
        - **Click the `Save image` button** on the new window to download the full-resolution image.
        - Enjoy not paying for Arcaea Online!

## Quick Side Note

If some song jacket files are missing, feel free to add them yourself in the `arcaea_song_files` directory. The song
jacket file has to meet these following criteria:

- The file extension is `.jpg`.
- The file name is in lower-case.
    - For example, `HELLOHELL.jpg` &#8594; `hellohell.jpg`
- All spaces are replaced with underscores
    - For example, `Abstruse Dilemma.jpg` &#8594; `abstruse_dilemma.jpg`
- The following symbols are removed:
    - `!`, `*`, `#`, `[`, `]`, `?`, `:`, `,`, `|`
- For non-unicode song names, add another item with the updated, unicode-friendly song name in the `nonunicode.json`
  file.
    - For example, `{ ..., "ω4": "w4"}`

## Contributing

Contributions are welcome with open hands! If you find any bugs or have suggestions, please open an issue or submit a
pull request.

## Contact

Additionally, suggestions and feedback can be sent directly to me at:

- Discord: sakurahikxri

## License

This project is licensed under the [MIT License](LICENSE.txt).
