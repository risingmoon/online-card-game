
filename="packages.txt"
packages=""
while read -r package;do
    echo "here $package";
    packages="$packages $package";
done < $filename
sudo apt-get update
sudo apt-get install$packages