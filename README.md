# Auto Read QR Code/Barcode (On Screen) And Input On Webpage/Text File

This program uses OBS Virtual Cam plugin to read the QR Code shown on screen, it can be modified to use webcam or other external camera. The program also input the qr code on website automatically.

- [Prerequisites](#prerequisites)
- [To Do](#ToDo)
- [Configuration options](#configuration-options)
- [Run the script](#run-the-script)

## Prerequisites  
- Python3 ([Download](https://www.python.org/downloads/))  
- OBS Studio ([Download](https://obsproject.com/))  
- OBS-VirtualCam Plugin ([Download](https://obsproject.com/forum/resources/obs-virtualcam.539/))

## ToDo
- [ ] Delay Time To Start Next Scan
- [ ] Auto run OBS

## Configuration Options
- **website:** The website that you want the QR code/Barcode to be key in. If you leave it empty，the QR code will be written to result.txt instead.

- **screenshot:** If this option is true, the program will screenshot the webpage or text file after 10 seconds inputting the code.

- **screenshot_path:** The folder that you want the screenshot to be saved in. If you leave it empty, the screenshots will save to the program folder in default. Example: C:\\Desktop

- **regex_format:** The regular expression that you want the QR code/Barcode to match. If you leave it empty, there will not be a constraint of format for QR code/Barcode.

- **avoid_duplicate:** If this option is true, the program will not read the current QR code/Barcode result if it is the same as the last result.

<!-- - **idle_time:**  The seconds that you want the program to wait for before scanning in another QR code/Barcode. Set this option to 0 if you don't want a delay on reading the QR code/Barcode. Only integer is allowed. -->
- **discord_webhook_url:** The Discord's webhook will update the qr code or barcode result and the screenshot of the website (if specify) in the specified Discord server. If you don't need it, leave it blank.

- **discord_message:** Discord message can be a mention to the user or anything that you would like to add.
<!-- - **auto_start_obs:** If this option is true, the program will auto start OBS Studio to read the result. Set this to false if you prefer to open it manually or you want to use other camera. -->

- **camera_position:** By default, the program will use the 2nd camera that is found in the system, which should be the OBS-VirtualCam. You may adjust it if your desired camera position is not at 2.
<!-- - **another_key:** -->

- **input_class_name:** If you are entering data in a website, here is the input class name so the program will wait until the input is available and click to focus on it.

- **auth_data:** By default it is blank, if the website needs verification, please modify this into "user-data-dir=C:\\Users\\YOURUSERNAME\\AppData\\Local\\Google\\Chrome\\User Data"

- Dangerous Configuration Options: **delay_start_ie**, **delay_connect_ie**, **delay_focus_ie**, **delay_input_ie**, **delay_process_ie**, **delay_kill_ie**

    The program uses Google Chrome to input QR Code/Barcode. The following option should only be modified if you are confident of the responding time. These options are not applicable if you leave the **website** option blank.

## Run the script

 1. Modify "config.json" to fit your preference
 2. Install dependencies:   ```pip install -r requirements.txt```
 3. Download chromedriver.exe into bin folder. 
 4. Setup OBS Virtual Cam
 5. Run [auto_scan_input_code.py](auto_scan_input_code.py): `python auto_scan_input_code.py`
