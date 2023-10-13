# PC2_Graphic_Computing

## Parte 1
En esta sección, desarrollamos una página web para cargar imágenes y, de esta manera, generar el dataset con el cual entrenaremos nuestro modelo. La funcionalidad de la página web consiste en lo siguiente: en la página principal, se muestra un lienzo (canvas) que permite a los usuarios dibujar imágenes que posteriormente se emplearán en el proceso de entrenamiento. El procedimiento implica presionar el botón "Enviar" para guardar la imagen o "Borrar" para eliminar lo dibujado y, luego, el botón "Preparar" para consolidar las imágenes en dos archivos con formato .npy que deben ser descargadas a través de las rutas /X.npy y /y.npy.

## Parte 2
En esta etapa, procedimos a entrenar el modelo de forma local utilizando el archivo "model_training.ipynb". Tomando como base el código proporcionado en el ejemplo, lo ajustamos para que el modelo sea capaz de predecir el tipo de emoticono dibujado.

## Parte 3
Para el proceso de predicción, utilizamos la página web mencionada anteriormente, pero esta vez empleamos la ruta "predict". En la ruta "/predict", se puede dibujar una imagen en el lienzo y, al presionar el botón "Predecir", se llama a nuestra API para realizar la predicción del dibujo utilizando el modelo que hemos entrenado.
