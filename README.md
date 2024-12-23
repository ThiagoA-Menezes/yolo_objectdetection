# YOLO Object Detection
![GitHub stars](https://img.shields.io/github/stars/ThiagoA-Menezes/yolo_objectdetection)
![GitHub license](https://img.shields.io/github/license/ThiagoA-Menezes/yolo_objectdetection)

## Sobre o Projeto
Este projeto implementa um sistema de **detecção de objetos** utilizando o algoritmo YOLO (You Only Look Once). Ideal para aplicações em visão computacional, como segurança, monitoramento e análise de vídeo em tempo real.

## Demonstração
![Demo](https://b2633864.smushcdn.com/2633864/wp-content/uploads/2018/11/yolo_living_room_output.jpg?lossy=2&strip=1&webp=1)

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/ThiagoA-Menezes/yolo_objectdetection.git

2. Criei um ambiente virtual
   ```bash
   python -m venv yolo_venv

3. Inicie o Virtual Environment:
   ```bash   
   source yolo_venv/bin/activate

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt

5. Execute o Projeto
   ```bash
   python main.py

## Como Usar
1. Insira as imagens na pasta `inputs/`.
2. Execute o script e visualize os resultados na pasta `outputs/`.
    ```bash
    python detect_objects.py --image inputs/sample.jpg

## Funcionalidades
- Detecta objetos em imagens e vídeos.
- Suporte a múltiplos formatos de entrada.
- Interface gráfica simples e intuitiva (opcional).

## Tecnologias
- Python 3.12
- OpenCV
- PyTorch

## Contribuição
Contributions são bem-vindas! Siga os passos abaixo:
1. Faça um fork do projeto.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b minha-feature

## Contato
Thiago Menezes - [LinkedIn](https://www.linkedin.com/in/thiagoamenezes/)  
Email: assis.thiago@gmail.com 