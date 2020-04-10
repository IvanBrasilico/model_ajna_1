
Os prodedimentos abaixo foram efetuados no Servidor 10.68.90.100 (CentOS 7)

Os arquivos utilizados (cuda-repo, libcudnn e driver Nvidia) estão em /home/ivan. O restante foi instalado via yum.

1 . Baixar o driver correto (no caso Liunx 64bit) do site da Nvidia.

https://www.geforce.com/drivers

2. Instalar pre-requisitos e desabilitar driver nouveau

https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-centos-7-linux

```
lshw -numeric -C display (Vai mostrar nouveau)
yum groupinstall "Development Tools"
yum install kernel-devel epel-release
yum install dkms
sudo nano /etc/grub/  (GRUB_CMDLINE_LINUX="crashkernel=auto rhgb quiet *nouveau.modeset=0 modprobe.blacklist=nouveau*")
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
sudo grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
sudo reboot
lshw -numeric -C display (Vai ter desaparecido nouveau)
```

3. Instalar drivers Nvidia
```
systemctl isolate multi-user.target (necessário apenas se houver Servidor X instalado)
sudo yum install "kernel-devel-uname-r == $(uname -r)" (Este comando só é necessário se a instalação da Nvidia falhar reclamando falta de headers do kernel)
bash NVIDIA-Linux-x86_64-*
```

4. Instalar CUDA
https://gist.github.com/Mahedi-61/e0625c8782426168e436fb98417ef209
```
### to verify your gpu is cuda enable check
lspci | grep -i nvidia

### gcc compiler is required. Se não presente, instalar com yum install gcc
gcc --version

# O nome do arquivo abaixo tem que ser pego no site da Nvidia. É preciso baixar a versão mais atual/compatível
# a placa de vídeo instalada
wget https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/cuda-repo-rhel7-10.0.130-1.x86_64.rpm

# install the packages
sudo rpm -i cuda-repo-rhel7-10.0.130-1.x86_64.rpm

# install cuda
sudo yum install cuda

# setup your paths
echo 'export PATH=/usr/local/cuda-10.0/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
sudo ldconfig

# install cuDNN 
# in order to download cuDNN you have to be regeistered here https://developer.nvidia.com/developer-program/signup
# then download cuDNN v7.5 form https://developer.nvidia.com/cudnn
# O nome do arquivo abaixo tem que ser pego no site da Nvidia. É preciso baixar a versão mais atual/compatível
# a placa de vídeo instalada E com a versão do CUDA instalado
wget https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.5.0.56/prod/10.0_20190219/cudnn-10.0-linux-x64-v7.5.0.56.rpm
sudo rpm -i cudnn-10.0-linux-x64-v7.5.0.56.rpm

# Finally, to verify the installation, check
nvidia-smi
nvcc -V

# install Tensorflow (an open source machine learning framework)
# I choose version 1.13.1 because it is stable and compatible with CUDA 10.0 Toolkit and cuDNN 7.5
sudo yum install python3.6
sudo pip3 install --user tensorflow-gpu pandas sklearn requests 
```
