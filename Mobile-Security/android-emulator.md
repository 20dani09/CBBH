# Android emulator

```bash
sudo apt install adb snapd
systemctl start snapd.service
```

adb: android debug bridge
## Anbox

Nota histórica: Anbox está archivado y es de solo lectura desde el 13 de febrero de 2024. Se conserva la instalación original para documentar el entorno antiguo; no se ha validado que funcione hoy. [Estado oficial del proyecto](https://github.com/anbox/anbox).

https://github.com/anbox/anbox

```bash
git clone https://github.com/anbox/anbox.git --recurse-submodules
cd anbox
mkdir build
cd build
cmake ..
make
```

```bash
snap install --devmode --beta anbox 
```


### install apk

```bash
adb install file.apk
```


### burpsuite

```bash
adb shell settings put global http_proxy 10.10.14.29:8001
```

[Captura pendiente de revisión: Pasted image 20240531105209.png](../Resources/Audit/media.csv)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| pentestNotes | Android/Android emulator.md | ea46064dea8893ed6d54216151ae1bb0ef3661ba |

[Índice de categoría](README.md) · [Inicio](../README.md)
