# Flowise Database Synchronization

This project is a tool to synchronize Flowise database with Supabase. This way you can store and manage your Flowise database on different platforms.

## Installation and Use

### 1. Creating a Virtual Environment and Package Installation

Create a virtual environment in the Flowise directory and install the required packages:

```bash
cd /home/ubuntu/Flowise
python3 -m venv myenv
source myenv/bin/activate
pip install supabase schedule
```

### 2. Installing the Python File

Upload the Python file `synchronous.py` to the Flowise directory or create a new file in the existing directory and paste its contents.

### 3. Supabase Database Installation

1. Create a new database on Supabase.
2. Open the SQL editor from the left menu.
3. Copy the SQL commands from the `sql_code` file and run them in the Supabase SQL editor.
4. Copy your Supabase URL and API key from the project settings.
5. Paste this information into the corresponding places in the `synchron.py` file.
6. Specify the correct `database.sqlite` directory path in `synchron.py`.

### 4. Running the script

```bash
python synchron.py
```

The script is executed with this command. The system will automatically synchronize the database every two minutes.

## Autorun (Optional)

You can create a system service so that the script runs automatically when the server starts:

1. Create a service file:

```bash
sudo nano /etc/systemd/system/system/database_sync.service
```

2. Add the following content to the file:

```ini
[Unit]
Description=Database Synchronization Service

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Flowise
ExecStart=/home/ubuntu/Flowise/myenv/bin/python <SENKRON.PY_FILE_PATH>
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Activate and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable database_sync.service
sudo systemctl start database_sync.service
```

4. Check the service status:

```bash
sudo systemctl status database_sync.service
```

## Debug

If you encounter problems during synchronization:

1. Make sure that the information in the `.env` file is correct.
2. Check the Supabase and SQLite database connections.
3. Examine the error messages in the `synchron.py` file.
4. If necessary, add more detailed logging to `synchron.py`.

## Security Notes

- Don't forget to add `.env` to your `.gitignore` file.
- Consider using a more secure secret management solution in a production environment.

## Database Backup

It is recommended to back up your SQLite database before the synchronization process starts:

```bash
cp /path/to/your/database.sqlite /path/to/your/database_backup_$(date +%Y%m%d_%H%M%S).sqlite
```

You can add this command to the beginning of your `sync.py` script or create a separate backup script.


## Notes

- This README file describes the setup and use of your project. You can update or extend it as needed.
- If you want to change the synchronization frequency, you can update the corresponding parameter in the `sync.py` file.

## Contributing

If you would like to contribute to the project, please open a Pull Request or create an Issue.
