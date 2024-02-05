import src.youfucktube as youfucktube
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
import webbrowser
import threading
import pyperclip
import requests
import re

executar_monitoramento = True

def main():
    global err_msg
    app = tk.Tk()
    app.title("BlockAds")
    app.geometry("290x230")
    app.configure(bg="#252526")
    app.resizable(False, False)

    def fechar_programa():
        global executar_monitoramento
        executar_monitoramento = False
        app.destroy()
    app.protocol("WM_DELETE_WINDOW", fechar_programa)

    spacer_label = tk.Label(app, fg="#dadf49", bg="#252526").pack()
    url_imagem = "https://cdn3d.iconscout.com/3d/premium/thumb/ad-blocked-6506863-5379627.png?f=webp"
    resposta = requests.get(url_imagem)
    imagem_bytes = BytesIO(resposta.content)
    imagem_pil = Image.open(imagem_bytes)
    nova_dimensao = (50, 50)
    imagem_pil.thumbnail(nova_dimensao)
    imagem_tk = ImageTk.PhotoImage(imagem_pil)
    app.iconphoto(True, imagem_tk)
    label_imagem = tk.Label(app, image=imagem_tk, bg="#252526", cursor='hand2')
    label_imagem.pack()
    label_imagem.bind("<Button-1>", lambda event: abrir_link())

    normal_font = ("Helvetica", 10)
    bold_font = ("Helvetica", 12, "bold")
    spacer_label = tk.Label(app, fg="#dadf49", bg="#252526").pack()
    input_label = tk.Label(
        app, text="Youtube BlockAds:", font=bold_font, fg="white", bg="#252526"
    )
    input_label.pack()
    # url = tk.Entry(app, width=35, font=normal_font, justify="center", borderwidth=3)
    # url.pack()
    err_msg = tk.StringVar()
    spacer_label2 = tk.Label(app, text="", bg="#252526").pack()

    def button_press():
        err_msg.set("")
        conteudo_anterior = ""
        conteudo_atual = pyperclip.paste()
        try:
            if conteudo_atual != conteudo_anterior:
                if eh_link_do_youtube(conteudo_atual):
                    video_id: str = youfucktube.extract_video_id(conteudo_atual)
                    link = youfucktube.create_link(video_id)
                    youfucktube.open_browser(link)
                    conteudo_anterior = conteudo_atual
                    return
        except ValueError:
            err_msg.set("Please input a valid youtube URL.")
            return

    def abrir_link():
        link = "https://github.com/KauanSantosCunha/block_ad"  # Substitua pelo seu link desejado
        webbrowser.open(link)

    submit_button = tk.Button(
        app,
        text="Submit",
        command=button_press,
        font=bold_font,
        bg="#007acc",
        fg="white",
        borderwidth=1,
        cursor='hand2'
    )
    submit_button.pack()

    warning_label = tk.Label(
        app, textvariable=err_msg, fg="#dadf49", bg="#252526", font=normal_font
    )
    warning_label.pack()
    spacer_label = tk.Label(app, text="IPMCCD by @Dev_Kauan", fg="#dadf49", bg="#252526").pack()

    threading.Thread(target=monitorar_area_transferencia).start()
    app.mainloop()

def monitorar_area_transferencia():
    conteudo_anterior = ""
    while executar_monitoramento:
    # while True:
        conteudo_atual = pyperclip.paste()
        if conteudo_atual != conteudo_anterior:
            if eh_link_do_youtube(conteudo_atual):
                video_id: str = youfucktube.extract_video_id(conteudo_atual)
                link = youfucktube.create_link(video_id)
                youfucktube.open_browser(link)
                conteudo_anterior = conteudo_atual
                err_msg.set(video_id)

def eh_link_do_youtube(texto):
    # Padrão básico para identificar URLs do YouTube
    padrao_youtube = re.compile(r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/.+$')
    return padrao_youtube.match(texto) is not None


if __name__ == "__main__":
    main()
