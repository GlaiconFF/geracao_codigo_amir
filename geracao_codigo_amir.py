import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import subprocess

sumatra = r"C:\Users\Usuário\AppData\Local\SumatraPDF\SumatraPDF.exe"
printer = "HP LaserJet MFP E42540 [988D9B]"

pdf_path = r'AMIR\amir.pdf' #Local do arquivo
poppler_path = r'C:\Program Files\poppler-24.08.0\Library\bin'

paginas = convert_from_path(pdf_path, poppler_path=poppler_path)
imagem_pil_base = paginas[0]
imagem_cv_base = cv2.cvtColor(np.array(imagem_pil_base), cv2.COLOR_RGB2BGR)

fonte = cv2.FONT_HERSHEY_DUPLEX
escala = 2
cor = (0, 0, 0)
espessura = 2

with open(r'AMIR\numeracao_amir.txt', 'r') as arquivo:
    texto = int(arquivo.read())
    print(texto)

dest_x = 170
dest_y = 100

paginas_pdf = []

for i in range(30):
    imagem_escrever = imagem_cv_base.copy()
    texto_str = str(texto)
    texto += 1

    (w, h), _ = cv2.getTextSize(texto_str, fonte, escala, espessura)
    text_img = np.ones((h + 10, w + 10, 3), dtype=np.uint8) * 255
    cv2.putText(text_img, texto_str, (5, h + 2), fonte, escala, cor, espessura, cv2.LINE_AA)

    text_img_rotated = cv2.rotate(text_img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    h_t, w_t, _ = text_img_rotated.shape
    if dest_y + h_t <= imagem_escrever.shape[0] and dest_x + w_t <= imagem_escrever.shape[1]:
        imagem_escrever[dest_y:dest_y + h_t, dest_x:dest_x + w_t] = text_img_rotated
    else:
        print("Texto fora dos limites da imagem!")

    imagem_pil = Image.fromarray(imagem_escrever)

    imagem_pil = imagem_pil.resize((2480, 3508))

    paginas_pdf.append(imagem_pil)

pdf_final = r"AMIR\imagem_final.pdf" #Local do arquivo

paginas_pdf[0].save(
    pdf_final,
    "PDF",
    resolution=300.0,
    save_all=True,
    append_images=paginas_pdf[1:]
)

print("PDF multipágina criado com sucesso!")

settings = "1x,simplex"

cmd = [
    sumatra,
    "-print-to", printer,
    "-print-settings", settings,
    pdf_final
]

print("Enviando impressão...")
subprocess.run(cmd, check=True)
print("Impressão enviada com sucesso!")

with open(r'AMIR\numeracao_amir.txt', 'w') as arquivo:
    arquivo.write(str(texto))
print(texto)