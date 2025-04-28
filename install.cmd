@echo off
:: Script para instalar dependências no WSL e adicionar opção "Executar all2pdf" ao menu de contexto
:: Execute como Administrador!

:: ========================================
:: 1. Comandos no WSL (Instalação do all2pdf)
:: ========================================
echo Instalando dependências no WSL...
wsl sudo apt update && wsl sudo apt install -y libreoffice-writer enscript ghostscript
wsl sudo chmod +x all2pdf.py
wsl sudo ln -s "$(pwd)/all2pdf.py" /usr/local/bin/all2pdf

:: ========================================
:: 2. Atualizações no Registro do Windows
:: ========================================
echo Atualizando registro do Windows...

:: Definições
set "REG_KEY=HKEY_CLASSES_ROOT\Directory\Background\shell\RunAll2PDF"
set "ICON_PATH=C:\Windows\System32\imageres.dll,-10"
set "COMMAND=wsl sudo su -c \"all2pdf\""

:: Adiciona a chave principal
reg add "%REG_KEY%" /ve /d "Executar all2pdf" /f

:: Define o ícone
reg add "%REG_KEY%" /v "Icon" /d "%ICON_PATH%" /f

:: Adiciona o comando
reg add "%REG_KEY%\command" /ve /d "%COMMAND%" /f

echo Instalação concluída! O all2pdf está pronto para uso.
pause