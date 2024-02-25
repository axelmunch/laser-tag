pyinstaller --clean --onefile --noconsole --workpath build --distpath dist --specpath build --name "Laser Tag" laser_tag/__main__.py
cp -r data dist

pyinstaller --clean --onefile --workpath build --distpath dist --specpath build --name "Laser Tag Server" laser_tag/network/Server.py
