## Running webapp on your local machine

Launch Flask webapp from your terminal using:
>> python main.py  

This will launch an internet browser window, or you can open it at http://127.0.0.1:5000/

The webapp has to be re-launched after any changes to the code. 





## Running webapp from Python Anywhere

The file structure is the same. The name of the file with the main webapp code, such as "main.py," must match what was provided as part of the webapp path or in the import statement in the WSGI configuration file. The files have to be imported into the pythonanywhere.com directory for the webapp. 

The webapp code has to be saved and re-loaded after any changes to the code (from the pythonanywhere webapp dashboard). 

The webapp is available at: http://resy.pythonanywhere.com/

#### For debugging

See the console output such as print statements in the [server log](https://www.pythonanywhere.com/user/resy/files/var/log/resy.pythonanywhere.com.server.log)

And pythonanywhere-generated erros in the [error log](https://www.pythonanywhere.com/user/resy/files/var/log/resy.pythonanywhere.com.error.log)

Pythonanywhere's Flask reference [page](https://blog.pythonanywhere.com/121/)  

