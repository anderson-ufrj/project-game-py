#!/usr/bin/env python3
"""
Script para corrigir perfis de cor incorretos em imagens PNG
Remove perfis sRGB problemáticos que causam warnings do libpng
"""
import os
import sys
from PIL import Image
import glob

def fix_png_icc_profile(file_path):
    """
    Remove perfil ICC problemático de um arquivo PNG
    
    Args:
        file_path (str): Caminho para o arquivo PNG
        
    Returns:
        bool: True se o arquivo foi corrigido, False caso contrário
    """
    try:
        # Abrir imagem
        with Image.open(file_path) as img:
            # Verificar se tem perfil ICC
            if 'icc_profile' in img.info:
                print(f"🔧 Corrigindo perfil ICC: {os.path.basename(file_path)}")
                
                # Criar nova imagem sem perfil ICC
                new_img = img.copy()
                
                # Remover perfil ICC problemático
                if 'icc_profile' in new_img.info:
                    del new_img.info['icc_profile']
                
                # Salvar imagem corrigida
                new_img.save(file_path, 'PNG', optimize=True)
                return True
            else:
                print(f"✅ Sem perfil ICC: {os.path.basename(file_path)}")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False

def find_and_fix_png_files(root_dir):
    """
    Encontra e corrige todos os arquivos PNG em um diretório
    
    Args:
        root_dir (str): Diretório raiz para buscar arquivos PNG
    """
    # Padrões de busca
    png_patterns = [
        os.path.join(root_dir, '**', '*.png'),
        os.path.join(root_dir, '**', '*.PNG')
    ]
    
    total_files = 0
    fixed_files = 0
    
    print(f"🔍 Buscando arquivos PNG em: {root_dir}")
    
    for pattern in png_patterns:
        for file_path in glob.glob(pattern, recursive=True):
            # Pular arquivos temporários e backups
            if any(skip in file_path for skip in ['.git', '__pycache__', '.tmp', '.bak']):
                continue
                
            total_files += 1
            if fix_png_icc_profile(file_path):
                fixed_files += 1
    
    print(f"\n📊 Resumo:")
    print(f"   Total de arquivos PNG: {total_files}")
    print(f"   Arquivos corrigidos: {fixed_files}")
    print(f"   Arquivos sem problemas: {total_files - fixed_files}")
    
    if fixed_files > 0:
        print(f"\n✅ {fixed_files} arquivos PNG foram corrigidos!")
        print("   Os warnings 'libpng warning: iCCP: known incorrect sRGB profile' devem parar.")
    else:
        print("\n✅ Nenhum arquivo PNG precisou ser corrigido.")

def main():
    """Função principal"""
    # Diretório do projeto
    project_dir = '/home/anderson-henrique/Documentos/project-game-py'
    
    if not os.path.exists(project_dir):
        print(f"❌ Diretório não encontrado: {project_dir}")
        sys.exit(1)
    
    print("🖼️ Corretor de Perfis PNG")
    print("=" * 50)
    print("Este script remove perfis ICC problemáticos de arquivos PNG")
    print("que causam warnings do libpng.")
    print()
    
    # Processar arquivos
    find_and_fix_png_files(project_dir)
    
    print("\n🎉 Processamento concluído!")
    print("Execute o jogo novamente para verificar se os warnings sumiram.")

if __name__ == "__main__":
    main()