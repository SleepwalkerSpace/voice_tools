# voice_tools

## Centos8安装FFmpeg
sudo dnf install epel-release
sudo yum config-manager --set-enabled PowerTools
sudo yum-config-manager --add-repo=https://negativo17.org/repos/epel-multimedia.repo
sudo dnf install ffmpeg --nogpgcheck
ffmpeg -version