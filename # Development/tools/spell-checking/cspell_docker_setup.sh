apt update --assume-yes || exit $?
apt install python3 --assume-yes || exit $?
apt install npm --assume-yes || exit $?
npm install --global cspell || exit $?
