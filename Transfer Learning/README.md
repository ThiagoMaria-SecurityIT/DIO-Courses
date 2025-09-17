#  Desafio DIO: Transfer Learning em uma rede de Deep Learning 

## Overview
Esse README é para entrega do projeto do curso da `DIO` (BairesDev - Machine Learning Training).  

## Objetivos do projeto:
- Aplicar o método de Transfer Learning em uma rede de Deep Learning
- Utilizar a linguagem Python
- Utilizar o ambiente COLAB.

## Objetivos de Aprendizagem   
- Aplicar os conceitos aprendidos em um ambiente prático;   
- Documentar processos técnicos de forma clara e estruturada;  
- Utilizar o GitHub como ferramenta para compartilhamento de documentação técnica;  

## Entendo como fazer o Transfer Learning  
De modo geral, a aprendizagem por transferência se refere ao processo de aproveitar o conhecimento aprendido em um modelo para o treinamento de outro modelo.

Mais especificamente, o processo envolve pegar uma rede neural existente, previamente treinada para um bom desempenho em um conjunto de dados maior, e usá-la como base para um novo modelo que aproveita a precisão dessa rede anterior para uma nova tarefa. 

O ponto chave da parte técnica é entender como `congelar` as weights e utilizar as layers para treinar uma rede neural menor e melhor.


### Transfer learning
Pode envolver pegar a rede pré-treinada e *congelar* os weights como uma feature extraction, usando essa feature como entrada para uma rede neural menor.

### Fine-Tunning
Pode envolver pegar a rede pré-treinada e congelar os weights, e usar uma de suas layers ocultas (geralmente a última) como um extrator de recursos (feature extraction), usando esses recursos como entrada para uma rede neural menor.   

## Começando
De forma simplificada, podemos falar que com esses dois conceitos em mente (congelar as weights e utilizar as layers), temos como começar o projeto.  
Para começar, vou escolher uma base de dados:

- Continua nos próximos dias
