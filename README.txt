This project aims to recognize faces from a Google drive on a local machine. The faces are recognized and a unique log is created everyday.
For example: Today's hypothetical date is October 17th, 2024. After the script concludes, either by its time check or manual intervention, a log will be created with the name: log_2024-10-17.csv.
In this case, the format is log_ followed by year, month, and day. (Seperating these values is a '-')
How to operate script. The aim of the scripts is to create a nearly autonomous facial recognition platform.

MasterScript.py: This is the master script of the program, as outlined by name. To operate the MasterScript, the user must access its directory (Downloads). Simply accessing terminal and typing 'cd Downloads' will prompt the user to the directory (absolute path: /home/hayden/Downloads).
                 Starting this program the user must start the command with 'python'. In execution this will look like 'python MasterScript.py'. If the user is in the downloads diretory and executes this command the script will start.
                 The script begins by showing the current process ID, *note this ID will change upon each execution. Process ID is shown in the event of potential crashes. A simple 'kill' command followed by the PID will close the program.
                 After the PID is shown, the script will run. The script can take a while to execute as it is a bit resource intensive and has to fetch all the contents from a synced file before the webcam opens.
                 Next, the webcam will open on the left side of the screen. Simply click on the window to open the webcam.
                 The webcam will be a fourth of the screen size. Do NOT click on any of the buttons lining the top of the webcam application. This pop-up is built by python, therefore the buttons do not work or cause issues with the programming.
                 Move the webcam to the middle of the screen by clicking and dragging the window. Then access 'Universal Access' from settings. In the 'seeing' content box, click on 'Zoom' to open the screen magnificiation window.
                 Set Magnification to: 2.25. Then click the slider in the top right of the mini window turning it green.
                 Situate the screen to center the webcam feed.
                 Close tabs if desired.
                 
                 'MasterScript.py' is broken into two code segments.
                 First:
                 The first segment runs 'FaceRec.py' as a subprocess while simultaneously checking to see if it is currently running. If it is, nothing happens.
                 Second:
                 The second segment deals with time signature and flags. Essentially, it prepares the environment to run 'FaceRec.py' by instituting time based variables.
                 Times:
                 00:00 (12:00 AM). Environment is prepped with variables allowing the script to open. If variables are correct, the subprocess opens.
                 00:01 (12:01 AM). Subprocess is called as long as criteria meets set-up from 00:00.
                 The subprocess then runs till it closes itself at 23:59 (11:59 PM). 'FaceRec.py' closes itself at 23:59, environment is set for reopening at 00:00, and subprocess runs again at 00:01.
                 
                 User can safely manually close script by inserting 'Ctrl + C' in terminal. This will terminate 'MasterScript.py'. *Note, the user must then retype in 'python MasterScript.py' as manual intervention fully closes script.
                 Before manually closing 'MasterScript.py', close 'FaceRec.py', by passing the keystroke 'q' into the window. Closing out of order may result in bad computer performance.
                 Therefore manually closing revolves around:
                     Passing 'q' into webcam window.
                     *Note after webcam is closed, wait for log sheet to be created or appended before moving onto next step.
                     Passing 'Ctrl + c' into running terminal.
                 Closing the scripts in this order will yield proper results.
                 
FaceRec.py:      This is the operational script. It will take face encodings from the images in 'faces' and tag it with the files name. The information is stored in two arrays: 'face_encodings = []' and 'face_names = []'.
                 Arrays are processed before the webcam initializes, contributing to the pause before opening.
                 No direct input is needed for this program to work as it is called by the MasterScript.
                 High Priority Cases:      High Priority Cases are special individuals in the database.
                                           Identification of these individuals will cause special code to execute.
                                           Currently, identification of these individuals will cause a specified song to play.
                                           All names are stored in a dictionary called 'high_priority'.
                                           If you wish to add more High Priority Cases, the code has been simplified to make it as easy as possible.
                 Current High Priority Case code example: 
                 "Amazon": {
                     "first_identify": True,
                     "reset": None,
                     "timer": 10,
                     "audio": pygame.mixer.Sound('/home/hayden/Downloads/AudioTriggers/bbtrimmed.mp3')
                 }
                 'Amazon' is the name of the High Priority individual and must match the file name of the corrensponding image.
                 Otherwise, nothing will execute. The following entries: 'first_identify', 'reset', and 'timer' are actually unique variables corresponding to the current dictionary entry.
                 The only variables you need to change are 'audio' and 'timer'. Set 'audio' to the absolute path of the song you want to play and 'timer' to the length of the selected song.
                 Setting 'timer' perfectly is not imperative more of a cleanliness aspect.
                 Final note, make sure to seperate dictionary entries with a ','.
                 Copying this code and tweaking the aspects above ensures easy additions to the 'high_priority' dictionary.
                 
                 This script will autoclose itself everyday at 23:59 or 11:59 PM. The webcam will autoclose and all the log created will be consolidated to the log file mentioned above.
                 The time 23:59 is imperative to keeping accurate date logs.
                 Upon closing, 'MasterScript.py', will reopen the script as a subprocess at 00:01, or 12:01 AM. There is no need for human intervention.
                 Downtime between script closing itself and re-executing allows for folder, 'faces' to update with new entries.
                 
NameCounter.py:  The third script is not imperative to success with the program. Moreover, it acts as an extra feature for the log files.
                 'NameCounter.py' counts the occurence of each name in the log files. I.E. if there are a lot of logs for people it will count the occurence of each name and log them.
                 Example: Below will contain a sample log to showcase this scripts function.
                 Amazon detected at 2024-10-17 10:32:45
                 Amazon detected at 2024-10-17 10:33:55
                 Amazon detected at 2024-10-17 10:36:49
                 ElonMusk detected at 2024-10-17 10:40:50
                 Amazon detected at 2024-10-17 10:44:32
                 JacobRegnier detected at 2024-10-17 10:53:03
                 
                 The text below will be appended to the end of the log file:
                 
                 Name detection counts:
                 ElonMusk detected 1 times
                 Amazon detected 4 times
                 JacobRegnier detected 1 times
                 
                 This text makes the logs even more readable and gives an accurate count from the days logs.
                 'NameCounter.py' acts independently meaning the user must run it like 'MasterScript.py' (python NameCounter.py).
                 Upon execution, the script will show all logs in the current directory and take user input as to which file to make the aformentioned appening to.
                 After typing the file, i.e. 'log_2024-10-17.csv', there will be no further output and the user can easily see additions through 'cat 'log_name''.
                 
Folder Filing:   There are two necessary folders to implement this project: 'faces' and 'ffaces'. The folder: 'ffaces' is a local folder synced to a Google Drive folder.
                 Using 'rclone', and setting the path to the correct folder seed found in the Google drive, allows a local folder to be synced a cloud folder.
                 Contents are stored locally to 'ffaces' and then locally syned to 'faces'. This appears redundant, however, in the event of internet loss, it allows the program to continue proper execution.
                 Intricacies:
                 First, using 'rclone browser', found by searching in home taskbar, the user is prompted to the 'rclonebrowser' gui. Double click 'ffaces', it is the only remote in the query.
                 Only a segment of a Google drive is presented, navigate to 'upload stuff (File responses)' then 'Upload an image of your face. (Look at panel below for guidelines) (File responses)'.
                 Right click this folder and select 'Mount' from the dropdown menu.
                 Navigate to 'Downloads' and select 'ffaces' and singularly click to select the folder.
                 Look top right and select 'Open'.
                 This local folder and Google Drive folder are now synced.
                 A job is already configured to sync Google drive uploads to the local folder. However, this sync is connection dependant meaning if internet is lost you will not be able to access Google drive folder contents.
                 The folder 'ffaces' will be empty without this connection or if the 'rclone browser' is closed as this will terminate the running sync job.
                 Leave this window open in the background to have the 'faces' folder consistenetly updated.
                 Since internet connection should not be mandatory for this project, a crontab is created which uses 'rsync' to update the folder 'faces'.
                 This crontab is not reliant on a connection and will run every minute of every day.
                 Essentially, it will update 'faces' with new contents from 'ffaces' and since it is now saved in this new spot locally, there are no implications of connection.
                 The folder are now up to date with new contents to the Google drive.
                 
Google Drive:    Google drive is the cloud storage for the project. The user submits a Google form where they are prompted to enter a name and an image of themselves.
                 A Google App Script will rename their file input to their inputted name.
                 The App Script allows cleans up the name. For example: Hayden Amazon becomes HaydenAmazon and the image renames to HaydenAmazon.image.
                 The aformentioned App Script runs whenever a form is submitted.
                 Finally, the Google form is presented as a QR code allowing users to scan in their results from their devices.

We now have a way to collect names and files from someones' personal device, store them on a Google drive folder, and sync the uploads to a local folder.
Their uploads are formatted to make the transition from Google drive to folder to execute as seamless as possible.
Contents are saved on device in event of connection loss and are then read by the script. Time based events allow for proper chronological timing.

Overview:        Essentially the set-up is the following:
                 1. Open 'rclone browser' and mount 'Upload an image of your face. (Look at panel below for guidelines) (File responses)' to 'ffaces'.
                 2. Open 'terminal', 'cd Downloads', and 'python MasterScript.py'.

If there are any further questions, inquiries, or comments, reach out to me at 11026992@live.mercer.edu.     