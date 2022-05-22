echo "Install python and wget. wget is required for `n`"
apt update --assume-yes || exit $?
apt install python3 wget --assume-yes || exit $?

echo "Install latest and upgrade to latest npm version"
apt install npm --assume-yes || exit $?
npm install --global npm@latest || exit $?

echo "Upgrade node to latest version"
npm cache verify || exit $?
npm install --global n || exit $?
n stable || exit $?
hash -r || exit $?

echo "Install cspell"
npm install --global cspell || exit $?

echo "Setup completed successfully"
