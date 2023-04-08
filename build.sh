pyinstaller --clean --noconsole --workpath build --distpath dist --specpath build --name "Laser Tag" laser_tag/__main__.py
pyinstaller --clean --workpath build --distpath dist --specpath build --name "Laser Tag Server" laser_tag/network/Server.py
