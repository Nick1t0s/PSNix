# ffmpeg

> Набор инструментов для работы с аудио и видео из командной строки: конвертация, обрезка, монтаж, извлечение звука.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install ffmpeg -y
```

---

## Шаг 2 — Проверка

```bash
ffmpeg -version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`ffmpeg -i input.mkv out.mp4`|Конвертировать формат|
|`ffmpeg -i input.mp4 -vn out.mp3`|Извлечь звук из видео|
|`ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy cut.mp4`|Вырезать фрагмент без перекодирования|
|`ffprobe file.mp4`|Информация о файле|

---

## Устранение неполадок

### «Conversion failed!» при копировании

Убери `-c copy` — вероятно, формат не позволяет прямое копирование потоков, тогда нужно перекодирование.

---

## Ссылки

- [ffmpeg.org](https://ffmpeg.org/)
- [Документация ffmpeg](https://ffmpeg.org/documentation.html)
