pip uninstall acs-zeep-client -y
Remove-Item -Recurse -Force "acs-zeep-client"
git clone https://gitlabv3.thousandminds.com/zeep-apollo/fastapi-lib/acs-zeep-client.git
Remove-Item -Recurse -Force "acs-zeep-client\.git"
pip install -e acs-zeep-client