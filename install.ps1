# Script para instalar dependências no WSL e adicionar opção "Executar all2pdf" ao menu de contexto
# Execute como Administrador!

# ========================================
# 1. Comandos no WSL (Instalação do all2pdf)
# ========================================
Write-Host "Instalando dependências no WSL..." -ForegroundColor Cyan

# Verifica se o script está sendo executado como Administrador
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Execute este script como Administrador!" -ForegroundColor Red
    pause
    exit
}

# Comandos WSL
wsl sudo apt update && wsl sudo apt install -y libreoffice-writer enscript ghostscript
wsl sudo chmod +x all2pdf.py
wsl sudo ln -s "$(pwd)/all2pdf.py" /usr/local/bin/all2pdf

# ========================================
# 2. Atualizações no Registro do Windows
# ========================================
Write-Host "Atualizando registro do Windows..." -ForegroundColor Cyan

# Definições
$regKeyPath = "HKCR:\Directory\Background\shell\RunAll2PDF"
$iconPath = "C:\Windows\System32\imageres.dll,-10"
$command = 'wsl sudo su -c "all2pdf"'

# Cria a chave principal
New-Item -Path $regKeyPath -Force | Out-Null
Set-ItemProperty -Path $regKeyPath -Name "(Default)" -Value "Executar all2pdf"

# Define o ícone
Set-ItemProperty -Path $regKeyPath -Name "Icon" -Value $iconPath

# Cria a subchave 'command' e define o comando
New-Item -Path "$regKeyPath\command" -Force | Out-Null
Set-ItemProperty -Path "$regKeyPath\command" -Name "(Default)" -Value $command

Write-Host "Instalação concluída! O all2pdf está pronto para uso." -ForegroundColor Green
pause