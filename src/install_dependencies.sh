sudo pip3 install requests_oauthlib
sudo pip3 install pygeocoder
sudo pip3 install pygmaps --allow-external pygmaps --allow-unverified pygmaps

while true; do
    echo "Would you like to set Screlp as an alias? (yes/no)"
    read result
    if [ $result = "y" ] || [ $result = "yes" ]; then
        echo "Okey dokey!"
        alias screlp="python3 screlp.py"
        break
    elif [ $result = "n" ] || [ $result = "no" ]; then
        echo "Very well, then!"
        break
    else
        echo "Invalid response, please press y for yes or n for no."
fi
done