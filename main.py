from pytubefix import YouTube
from pytubefix.cli import on_progress
import streamlit as st
import os
from pdf2docx import Converter
from pdf2image import convert_from_path
import pandas as pd

#### CONFIGURAÇÃO INICIAL DA PÁGINA ####
st.set_page_config(page_title="Ferramentas do YouTube e Conversão de Arquivos", layout="wide")
st.image('youtube.png', width=300)
st.header('_Ferramentas de Download e Conversão_', divider="red")

# Criando abas
tabs = st.tabs(["Download do YouTube", "Conversor de Arquivos"])

with tabs[0]:
    ### INPUT DO VÍDEO ###
    video_url = st.text_input("Cole aqui o link do vídeo:")
    
    # Opção de download
    option = st.radio("Escolha o formato para download:", ('Áudio', 'Vídeo'))
    
    ### ATIVANDO O BOTÃO DE DOWNLOAD ###
    if st.button("Baixar"):
        if video_url:
            try:
                st.info("Baixando, aguarde...")
                yt = YouTube(video_url, on_progress_callback=on_progress)
                
                if option == 'Áudio':
                    stream = yt.streams.filter(only_audio=True).first()
                    out_file = stream.download()
                    
                    # Converter para mp3
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    st.success("Download de áudio concluído!")
                    st.write(f"Áudio salvo como **{os.path.basename(new_file)}**")
                    
                else:  # Download de vídeo
                    stream = yt.streams.get_highest_resolution()
                    out_file = stream.download()
                    st.success("Download de vídeo concluído!")
                    st.write(f"Vídeo salvo como **{os.path.basename(out_file)}**")

            except Exception as e:
                st.error(f"Erro ao baixar: {str(e)}")
        else:
            st.warning("Por favor, insira um link válido do YouTube.")

with tabs[1]:
    st.header("Conversor de Arquivos")
    uploaded_file = st.file_uploader("Envie um arquivo para conversão:")
    conversion_type = st.selectbox("Escolha o tipo de conversão:", [
        "PDF para DOCX", "PDF para Imagem", "PDF para Excel", "Imagem para PDF"])
    
    if uploaded_file and st.button("Converter"):
        try:
            if conversion_type == "PDF para DOCX":
                output_file = "output.docx"
                cv = Converter(uploaded_file)
                cv.convert(output_file)
                cv.close()
                st.success("Conversão concluída!")
                st.download_button("Baixar DOCX", output_file)
            
            elif conversion_type == "PDF para Imagem":
                images = convert_from_path(uploaded_file)
                for i, img in enumerate(images):
                    img.save(f"output_{i}.png", "PNG")
                st.success("Conversão concluída!")
                st.write("As imagens foram geradas com sucesso.")
                
            elif conversion_type == "PDF para Excel":
                output_file = "output.xlsx"
                tables = pd.read_html(uploaded_file)
                with pd.ExcelWriter(output_file) as writer:
                    for i, table in enumerate(tables):
                        table.to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)
                st.success("Conversão concluída!")
                st.download_button("Baixar Excel", output_file)
                
            elif conversion_type == "Imagem para PDF":
                output_file = "output.pdf"
                image = convert_from_path(uploaded_file)
                image[0].save(output_file, "PDF", resolution=100.0)
                st.success("Conversão concluída!")
                st.download_button("Baixar PDF", output_file)
        
        except Exception as e:
            st.error(f"Erro ao converter: {str(e)}")
