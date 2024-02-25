pyinstaller --clean --onefile --noconsole --workpath build --distpath dist --specpath build --name "Laser Tag" laser_tag/__main__.py
xcopy /e /i /y data dist\data

pyinstaller --clean --onefile --workpath build --distpath dist --specpath build --name "Laser Tag Server" laser_tag/network/Server.py
