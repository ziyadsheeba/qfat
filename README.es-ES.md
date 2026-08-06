

# Transformer de Acción Autoregresivo Libre de Cuantización

Una implementación oficial del artículo [**Transformer de Acción Autoregresivo Libre de Cuantización**](https://arxiv.org/abs/2503.14259v2). 

## Resumen
Los enfoques actuales de aprendizaje por imitación basados en transformers introducen representaciones discretas de acciones y entrenan un decodificador transformer autoregresivo sobre el código latente resultante. Sin embargo, la cuantización inicial rompe la estructura continua del espacio de acciones, lo que limita las capacidades del modelo generativo. En su lugar, proponemos un método libre de cuantización que aprovecha los Transformers de Vocabulario Infinito Generativo (GIVT) como una parametrización de  política directa y continua para transformers autoregresivos. Esto simplifica el pipeline de aprendizaje por imitación al tiempo que se logra un rendimiento de estado del arte en una variedad de tareas populares de robótica simulada. Mejoramos los despliegues de nuestra política mediante el estudio cuidadoso de los algoritmos de muestreo, mejorando aún más los resultados.

## Descripción de la Arquitectura
![qfat_policy](https://github.com/user-attachments/assets/16ea4b00-934b-4032-bd72-ffe4f9db6831)

## Instalación

Puede instalar este proyecto utilizando [Poetry](https://python-poetry.org/) o el archivo `requirements.txt`.

### Usando Poetry

Si prefiere administrar las dependencias con Poetry, siga estos pasos:

1. Instale Poetry si aún no lo tiene.

2. Navegue al directorio del proyecto e instale las dependencias:
   ```sh
   poetry install
   ```

3. Active el entorno virtual:
   ```sh
   poetry shell
   ```

### Usando `requirements.txt`

Alternativamente, puede instalar las dependencias utilizando `pip` y `requirements.txt`:

1. Cree y active un entorno virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

2. Instale las dependencias desde `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```
### Instalación de los Entornos Kitchen y UR3

Si está utilizando los entornos Kitchen o UR3, debe ejecutar el script de configuración para instalarlos correctamente:
   ```sh
   bash setup.sh
   ```
Esto asegurará que todas las dependencias y configuraciones necesarias para estos entornos se establezcan correctamente.

## Descarga de los Conjuntos de Datos

Este proyecto utiliza conjuntos de datos publicados en el artículo [VQ-BeT](https://arxiv.org/abs/2403.03181). Para comenzar:

1. Descargue el conjunto de datos desde la versión oficial: [Conjunto de Datos VQ-BeT](https://drive.google.com/file/d/1aHb4kV0mpMvuuApBpVGYjAPs6MCNVTNb/view?usp=sharing)
2. Cree un nuevo directorio llamado `data` dentro de su proyecto:
   ```sh
   mkdir data
   ```
3. Mueva todo el contenido del directorio del conjunto de datos al directorio `data`.

Si desea cambiar las rutas de los conjuntos de datos, puede ajustar las constantes de ruta en `src/qfat/constants.py`. 
Una vez que el conjunto de datos esté en su lugar, ¡ya está listo para continuar! 🚀 

## Inicio de Sesión en Weights & Biases

Este proyecto utiliza [Weights & Biases](https://wandb.ai/) (wandb) para el seguimiento de experimentos y el registro de modelos. Para configurar wandb, siga estos pasos:

1. Inicie sesión en wandb:
   ```sh
   wandb login
   ```

2. Siga las instrucciones para autenticarse con su cuenta de wandb.

## Ejecución del Entrenamiento

Para iniciar el entrenamiento de su modelo, utilice el siguiente comando:
   ```sh
   python scripts/train.py --config-name [CONFIG_NAME]
   ```

Reemplace `[CONFIG_NAME]` con uno de los nombres de configuración válidos que se encuentran en `configs/training`:

- `kitchen`
- `kitchen_conditional`
- `pusht_image`
- `pusht`
- `ur3`
- `ur3_conditional`
- `ant`

De forma predeterminada, los registros de entrenamiento y los puntos de control del modelo se rastrearán utilizando wandb. Puede personalizar la configuración de registro dentro de `config.yaml` o modificando el script de entrenamiento. Puede ajustar la frecuencia de guardado del modelo o la frecuencia de evaluación utilizando `n_save_model` y `n_eval`, respectivamente.

¡Asegúrese de haber iniciado sesión en wandb antes de ejecutar el entrenamiento para garantizar un seguimiento adecuado de los experimentos! 📊🔥

## Ejecución de la Inferencia

Una vez que haya entrenado los modelos, puede ejecutar la inferencia utilizando el siguiente comando:
   ```sh
   python scripts/inference.py --config-name [CONFIG_NAME]
   ```

Reemplace `[CONFIG_NAME]` con uno de los nombres de configuración válidos que se encuentran en `configs/inference`:

- `kitchen`
- `kitchen_conditional`
- `pusht_image`
- `pusht`
- `ur3`
- `ur3_conditional`
-  `ant`

Para ejecutar la inferencia correctamente, debe agregar el `training_run_id` de la sesión de entrenamiento en el archivo de configuración correspondiente dentro de `configs/inference`. Además, especifique el `model_afid` en el que desea ejecutar la inferencia. Tenga en cuenta que el nombre del artefacto debe coincidir con el formato `checkpoint_epoch_epochnumber_runid:v0`. 

Ejemplo de configuración:
```yaml
training_run_id: wandb_username/qfat/o4dz629x
model_id: wandb_username/qfat/checkpoint_epoch_720_o4dz629x:v0
```

## Callbacks

Los callbacks le permiten monitorear y depurar su modelo tanto durante el entrenamiento como la inferencia. Puede agregarlos a los archivos de configuración bajo `configs/training` y `configs/inference`. A continuación, se describen los **callbacks de inferencia** más importantes y cómo implementar los personalizados:

### Callbacks de Fin de Paso

Para visualizar las distribuciones de salida a lo largo del tiempo y registrarlas por dimensión como un video en wandb:
```yaml
callbacks:
  step_end:
    - _target_: qfat.callbacks.inference_callbacks.QFATOutputStatsLogger
      lim: [Add limits of the action space with a bit of buffer]
```
Esto ayuda a depurar y comprender lo que el modelo ha aprendido.

### Callbacks de Fin de Episodio

Para registrar la recompensa total al final de cada episodio:
```yaml
  episode_end:
    - _target_: qfat.callbacks.inference_callbacks.RewardLogger
      reward_reduction: sum  # Options: sum, last, average
```
Esto permite realizar un seguimiento del rendimiento del modelo a lo largo del tiempo.

Para registrar la distribución de éxito en la finalización de tareas y la entropía conductual:
```yaml
  episode_end:
    - _target_: qfat.callbacks.inference_callbacks.EnvBehaviourLogger
      min_sequence_length: # add minimum task completion sequence length you are interested in 
      max_sequence_length: # add maximum task completion sequence length you are interested in
```
Esto proporciona una perspectiva sobre el rendimiento de diferentes longitudes de secuencia.

### Callbacks Personalizados

Puede encontrar más opciones en `src/qfat/callbacks/inference_callbacks.py` para inferencia y `src/qfat/callbacks/training_callbacks.py` para entrenamiento. Hay muchas opciones de callback adicionales disponibles en estos archivos. Si se requiere una funcionalidad personalizada, implémentela allí y agréguela a una de las siguientes etapas para la inferencia:

- `step_start`
- `step_end`
- `episode_start`
- `episode_end`

y para el entrenamiento:

- `run_start`
- `run_end`
- `iteration_start`
- `iteration_end`
- `epoch_start`
- `epoch_end`
