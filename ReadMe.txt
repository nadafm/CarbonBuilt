sudo apt update
sudo apt-get update
sudo apt upgrade -y
sudo apt install git curl unzip tar make sudo vim wget -y
git clone https://github.com/nadafm/CarbonBuilt.git
sudo apt install python3-pip
pip3 install -r requirements.txt
#Temporary running
python3 -m streamlit run CarbonBuilt_latest.py