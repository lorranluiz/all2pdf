#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess

# Instalação das bibliotecas necessárias caso não estejam instaladas
def check_and_install_dependencies():
    try:
        print("Verificando dependências...")
        required_packages = ['tqdm', 'fpdf', 'docx2pdf', 'python-docx']
        missing_packages = []
        
        # Verifica quais pacotes estão faltando
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"Pacotes necessários não encontrados: {', '.join(missing_packages)}")
            print("\nNo Ubuntu moderno, há restrições para instalar pacotes via pip.")
            print("Para referência futura, estas são as opções de instalação:")
            
            # Opção 1: Ambiente virtual
            print("\nOPÇÃO 1: Criar um ambiente virtual (recomendado)")
            print("  sudo apt install -y python3-venv python3-full")
            print("  python3 -m venv ~/all2pdf_venv")
            print("  source ~/all2pdf_venv/bin/activate")
            print(f"  pip install {' '.join(missing_packages)}")
            
            # Opção 2: Pacotes apt
            print("\nOPÇÃO 2: Tentar instalar via apt")
            apt_packages = []
            for pkg in missing_packages:
                apt_packages.append(f"python3-{pkg.replace('-', '')}")
            print(f"  sudo apt install -y {' '.join(apt_packages)}")
            
            # Continua automaticamente com funções limitadas
            print("\nContinuando com funcionalidade limitada...")
            return True
        
        return True
    except Exception as e:
        print(f"Erro ao verificar dependências: {str(e)}")
        print("Continuando com possível funcionalidade limitada...")
        return True

# Tenta importar tqdm ou usa uma versão simplificada
if check_and_install_dependencies():
    try:
        from tqdm import tqdm
    except ImportError:
        # Versão simples de tqdm para uso sem a biblioteca
        def tqdm(iterable, **kwargs):
            print(f"{kwargs.get('desc', 'Processando')}: {len(iterable)} itens")
            for i, item in enumerate(iterable):
                print(f"Item {i+1}/{len(iterable)}: {os.path.basename(item)}")
                yield item
        
        # Versão simples da função tqdm.write
        def write(text):
            print(text)
        tqdm.write = write
else:
    sys.exit(1)

def find_convertible_files(directory):
    """
    Encontra todos os arquivos .txt, .doc e .docx no diretório especificado
    """
    convertible_files = []
    supported_extensions = ['.txt', '.doc', '.docx']
    
    for filename in os.listdir(directory):
        # Obtém a extensão do arquivo
        _, extension = os.path.splitext(filename)
        
        # Verifica se é um arquivo com extensão suportada
        if extension.lower() in supported_extensions:
            convertible_files.append(os.path.join(directory, filename))
    
    return convertible_files

def convert_txt_to_pdf(input_file, output_file):
    """Converte um arquivo TXT para PDF"""
    try:
        # Tenta a conversão com fpdf se estiver disponível
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as txt_file:
                for line in txt_file:
                    pdf.cell(200, 10, txt=line.strip(), ln=True)
            
            pdf.output(output_file)
            return True
        except ImportError:
            # Usa ferramentas do sistema se fpdf não estiver disponível
            print("Usando ferramentas do sistema para converter TXT para PDF...")
            
            # Verifica se enscript e ps2pdf estão instalados
            if subprocess.run("which enscript ps2pdf", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                cmd = f"enscript -p - \"{input_file}\" | ps2pdf - \"{output_file}\""
                result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    return True
                else:
                    print(f"Erro na conversão com enscript: {result.stderr.decode('utf-8')}")
            
            # Tenta usar pandoc se disponível
            elif subprocess.run("which pandoc", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                cmd = f"pandoc \"{input_file}\" -o \"{output_file}\""
                result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    return True
                else:
                    print(f"Erro na conversão com pandoc: {result.stderr.decode('utf-8')}")
            
            else:
                print("Ferramentas necessárias não encontradas. Instale com:")
                print("sudo apt install -y enscript ghostscript")
                print("ou")  
                print("sudo apt install -y pandoc texlive-latex-base")
                return False
            
    except Exception as e:
        print(f"Erro ao converter {input_file}: {e}")
        return False

def convert_docx_to_pdf(input_file, output_file):
    """Converte um arquivo DOC/DOCX para PDF"""
    try:
        # Tenta usar docx2pdf se disponível
        try:
            from docx2pdf import convert
            convert(input_file, output_file)
            return True
        except ImportError:
            # Usa LibreOffice como alternativa
            print("Usando LibreOffice para converter DOC/DOCX para PDF...")
            
            # Verifica se o LibreOffice está instalado
            if subprocess.run("which libreoffice", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                # Define o diretório de saída
                output_dir = os.path.dirname(os.path.abspath(output_file))
                base_name = os.path.basename(output_file)
                
                cmd = f"libreoffice --headless --convert-to pdf --outdir \"{output_dir}\" \"{input_file}\""
                result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
                
                if result.returncode == 0:
                    # LibreOffice mantém o nome original, apenas muda a extensão
                    input_base = os.path.splitext(os.path.basename(input_file))[0]
                    generated_pdf = os.path.join(output_dir, input_base + ".pdf")
                    
                    # Renomeia o arquivo se necessário
                    if generated_pdf != output_file and os.path.exists(generated_pdf):
                        os.rename(generated_pdf, output_file)
                    return True
                else:
                    print(f"Erro na conversão com LibreOffice: {result.stderr.decode('utf-8')}")
            
            # Tenta usar unoconv como alternativa
            elif subprocess.run("which unoconv", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                cmd = f"unoconv -f pdf -o \"{output_file}\" \"{input_file}\""
                result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
                
                if result.returncode == 0:
                    return True
                else:
                    print(f"Erro na conversão com unoconv: {result.stderr.decode('utf-8')}")
            
            else:
                print("Ferramentas necessárias não encontradas. Instale com:")
                print("sudo apt install -y libreoffice-writer")
                print("ou")
                print("sudo apt install -y unoconv")
                return False
                
    except Exception as e:
        print(f"Erro ao converter {input_file}: {e}")
        return False

def convert_file_to_pdf(input_file):
    """Converte qualquer arquivo suportado para PDF"""
    file_name, extension = os.path.splitext(input_file)
    output_file = file_name + ".pdf"
    
    if extension.lower() == ".txt":
        return convert_txt_to_pdf(input_file, output_file), output_file
    elif extension.lower() in [".doc", ".docx"]:
        return convert_docx_to_pdf(input_file, output_file), output_file
    else:
        return False, None

def main():
    # Cria um parser de argumentos
    parser = argparse.ArgumentParser(
        description='Converte arquivos .txt, .doc e .docx para PDF'
    )
    parser.add_argument(
        'directory', 
        nargs='?', 
        default=os.getcwd(),
        help='Diretório contendo arquivos para converter (padrão: diretório atual)'
    )
    args = parser.parse_args()
    
    # Usa o diretório fornecido ou o atual
    directory = args.directory
    
    print(f"Escaneando o diretório: {directory}")
    files_to_convert = find_convertible_files(directory)
    
    if not files_to_convert:
        print("Nenhum arquivo para converter encontrado.")
        return
    
    print(f"Encontrados {len(files_to_convert)} arquivos para conversão.")
    
    # Processa cada arquivo com barra de progresso
    for file_path in tqdm(files_to_convert, desc="Convertendo", unit="arquivo"):
        file_name = os.path.basename(file_path)
        tqdm.write(f"Convertendo: {file_name}")
        
        success, output_file = convert_file_to_pdf(file_path)
        
        if success and output_file:
            tqdm.write(f"✓ Convertido com sucesso: {os.path.basename(output_file)}")
        else:
            tqdm.write(f"✗ Falha ao converter: {file_name}")
    
    print("\nConversão concluída!")

if __name__ == "__main__":
    main()
