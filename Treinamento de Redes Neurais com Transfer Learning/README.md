# Projeto: Classificação de Imagens com Transfer Learning

### **Contexto do Projeto**

Este projeto foi desenvolvido como parte da jornada de aprendizado em Deep Learning, aplicando os conceitos estudados no bootcamp da DIO. O objetivo é demonstrar a aplicação prática da técnica de **Transfer Learning** para resolver um problema de classificação de imagens.  
A tarefa consiste em construir um modelo de alta performance capaz de distinguir entre imagens de gatos e cães, utilizando a biblioteca TensorFlow/Keras.  
Este `README.md` serve como a documentação técnica do projeto. Ele detalha o fluxo de trabalho completo, desde a configuração do ambiente e a preparação do dataset `cats_vs_dogs`, até a construção, o treinamento e a avaliação final do modelo.  

Cada seção descreve uma etapa do processo, explicando as decisões tomadas e apresentando os blocos de código correspondentes.  



## 📋 Índice
1.  [Introdução ao Transfer Learning](#1-introdução-ao-transfer-learning)
2.  [Configuração do Ambiente no Colab](#2-configuração-do-ambiente-no-colab)
3.  [Carregamento e Preparação do Dataset](#3-carregamento-e-preparação-do-dataset)
4.  [Pré-processamento e Aumento de Dados](#4-pré-processamento-e-aumento-de-dados)
5.  [Construção do Modelo com Transfer Learning](#5-construção-do-modelo-com-transfer-learning)
6.  [Treinamento em Duas Fases](#6-treinamento-em-duas-fases)
7.  [Avaliação do Modelo](#7-avaliação-do-modelo)
8.  [Conclusão e Próximos Passos](#8-conclusão-e-próximos-passos)

---

## 1. Introdução ao Transfer Learning

O **Transfer Learning (TL)** é uma técnica de Machine Learning que consiste em reutilizar um modelo pré-treinado em uma tarefa de grande escala (como a classificação de milhões de imagens do ImageNet) e adaptá-lo para um novo problema. Isso permite alcançar alta performance com menos dados e menor tempo de treinamento.

A ideia é que as camadas iniciais de uma rede neural convolucional (CNN) aprendem a detectar características genéricas (bordas, texturas, cores), que são úteis para diversas tarefas de visão computacional. Nós aproveitamos esses aprendizados e treinamos apenas as camadas finais para a nossa tarefa específica (gatos vs. cães).

---

## 2. Configuração do Ambiente no Colab

Primeiro, importamos as bibliotecas necessárias e verificamos a disponibilidade de uma GPU, o que acelera drasticamente o treinamento.

```python
# Importações principais
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import EfficientNetB0
import tensorflow_datasets as tfds

import numpy as np
import matplotlib.pyplot as plt

# Verifica a disponibilidade da GPU
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Configurações para garantir resultados reproduzíveis
SEED = 42
tf.random.set_seed(SEED)
np.random.seed(SEED)
```

---

## 3. Carregamento e Preparação do Dataset

Utilizamos o dataset `cats_vs_dogs` disponível no TensorFlow Datasets. Ele é automaticamente baixado e dividido em conjuntos de treino (80%), validação (10%) e teste (10%).

```python
# Carrega o dataset com as divisões
(ds_train, ds_validation, ds_test), ds_info = tfds.load(
    'cats_vs_dogs',
    split=['train[:80%]', 'train[80%:90%]', 'train[90%:]'],
    shuffle_files=True,
    as_supervised=True, # Retorna pares (imagem, label)
    with_info=True
)

# Exibe informações sobre o dataset
print(f"Número de classes: {ds_info.features['label'].num_classes}")
print(f"Nomes das classes: {ds_info.features['label'].names}")
print(f"Imagens de treino: {tf.data.experimental.cardinality(ds_train).numpy()}")
print(f"Imagens de validação: {tf.data.experimental.cardinality(ds_validation).numpy()}")
print(f"Imagens de teste: {tf.data.experimental.cardinality(ds_test).numpy()}")
```
**Saída esperada:**
```
Número de classes: 2
Nomes das classes: ['cat', 'dog']
Imagens de treino: 18610
Imagens de validação: 2326
Imagens de teste: 2326
```

---

## 4. Pré-processamento e Aumento de Dados

Para que as imagens possam ser usadas pelo modelo, elas precisam ser pré-processadas. Isso inclui:
*   **Redimensionamento:** Ajustar todas as imagens para o mesmo tamanho (`224x224` pixels).
*   **Normalização:** Converter os valores dos pixels de `[0, 255]` para `[0, 1]`.
*   **Aumento de Dados (Data Augmentation):** Aplicar transformações aleatórias (giros, zoom, etc.) apenas nas imagens de treino para que o modelo generalize melhor e evite overfitting.

```python
# Parâmetros
IMG_SIZE = (224, 224) # Tamanho de entrada para EfficientNetB0
BATCH_SIZE = 32
AUTOTUNE = tf.data.AUTOTUNE

# Camada para aumento de dados
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# Função para pré-processar as imagens
def preprocess_image(image, label):
    image = tf.image.resize(image, IMG_SIZE)
    image = tf.cast(image, tf.float32) / 255.0 # Normaliza para [0, 1]
    return image, label

# Função para preparar os datasets (aplicando pré-processamento e augmentation)
def prepare_dataset(dataset, is_training=False):
    dataset = dataset.map(preprocess_image, num_parallel_calls=AUTOTUNE)
    if is_training:
        dataset = dataset.shuffle(buffer_size=1000)
        dataset = dataset.map(lambda x, y: (data_augmentation(x), y), num_parallel_calls=AUTOTUNE)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(buffer_size=AUTOTUNE)
    return dataset

# Prepara os três conjuntos de dados
train_ds = prepare_dataset(ds_train, is_training=True)
val_ds = prepare_dataset(ds_validation)
test_ds = prepare_dataset(ds_test)
```

---

## 5. Construção do Modelo com Transfer Learning

Construímos nosso modelo usando a arquitetura **EfficientNetB0** como base.
1.  Carregamos o modelo pré-treinado no `ImageNet`, sem incluir sua camada classificadora final (`include_top=False`).
2.  **Congelamos** os pesos da base para que eles não sejam alterados na primeira fase de treino.
3.  Adicionamos um novo classificador no topo, com uma camada de saída `Dense` de 1 neurônio e ativação `sigmoid`, ideal para problemas de classificação binária.

```python
def create_model(input_shape=(224, 224, 3)):
    # Carrega o modelo base pré-treinado no ImageNet
    base_model = EfficientNetB0(
        include_top=False,
        weights='imagenet',
        input_shape=input_shape,
        pooling='avg'
    )

    # Congela a base para não ser treinada inicialmente
    base_model.trainable = False

    # Constrói o modelo final
    inputs = keras.Input(shape=input_shape)
    x = base_model(inputs, training=False) # Roda a base em modo de inferência
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(1, activation='sigmoid')(x) # Saída para classificação binária

    model = Model(inputs, outputs)

    # Compila o modelo
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model

# Cria o modelo
model = create_model()
model.summary()
```
*Note que a maioria dos parâmetros é "Non-trainable", o que é esperado na fase de extração de características.*

---

## 6. Treinamento em Duas Fases

O treinamento é dividido em duas etapas para obter os melhores resultados:

1.  **Feature Extraction:** Treinamos apenas o classificador que adicionamos. A base pré-treinada permanece congelada e atua como um extrator de características.
2.  **Fine-Tuning:** Após a primeira fase, descongelamos as últimas camadas da base e continuamos o treinamento com uma taxa de aprendizado (`learning_rate`) muito baixa. Isso permite que o modelo ajuste fino as características aprendidas para o nosso dataset específico.

```python
# --- Fase 1: Treinamento do Classificador ---
callbacks = [
    keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3)
]

history_feature_extraction = model.fit(
    train_ds,
    epochs=30,
    validation_data=val_ds,
    callbacks=callbacks
)

# --- Fase 2: Fine-Tuning ---
base_model = model.layers[1]
base_model.trainable = True

# Descongela apenas as últimas 30 camadas
for layer in base_model.layers[:-30]:
    if not isinstance(layer, layers.BatchNormalization):
        layer.trainable = False

# Recompila o modelo com uma taxa de aprendizado baixa
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Continua o treinamento
initial_epoch = len(history_feature_extraction.epoch)
history_fine_tuning = model.fit(
    train_ds,
    epochs=initial_epoch + 15,
    initial_epoch=initial_epoch,
    validation_data=val_ds,
    callbacks=callbacks
)
```

---

## 7. Avaliação do Modelo

Após o treinamento, avaliamos a performance final do modelo no conjunto de teste, que não foi utilizado em nenhuma etapa do treino ou ajuste. Isso nos dá uma medida real da capacidade de generalização do modelo.

```python
# Avalia no conjunto de teste
test_loss, test_accuracy = model.evaluate(test_ds)
print(f"\nAcurácia no teste: {test_accuracy * 100:.2f}%")

# Gera previsões para a matriz de confusão
y_true = np.concatenate([y for x, y in test_ds], axis=0)
y_pred_probs = model.predict(test_ds)
y_pred = (y_pred_probs > 0.5).astype(int).flatten()

# Plota a matriz de confusão e o relatório de classificação
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

cm = confusion_matrix(y_true, y_pred)
class_names = ds_info.features['label'].names
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Previsto')
plt.ylabel('Real')
plt.title('Matriz de Confusão')
plt.show()

print("\nRelatório de Classificação:")
print(classification_report(y_true, y_pred, target_names=class_names))
```
Com esta abordagem, é esperado alcançar uma **acurácia superior a 98%**.

Para salvar o modelo treinado, use o seguinte comando:
```python
# Salva o modelo
model.save('cats_vs_dogs_classifier.h5')
```
