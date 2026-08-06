# yt-dlp

> Загрузчик видео с YouTube и сотен других сайтов из командной строки (форк youtube-dl).

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install yt-dlp -y
```

Для самой свежей версии можно поставить через pip:

```bash
pip install --user -U yt-dlp
```

---

## Шаг 2 — Проверка

```bash
yt-dlp --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`yt-dlp "URL"`|Скачать лучшее качество|
|`yt-dlp -f mp4 "URL"`|Скачать в mp4|
|`yt-dlp -x --audio-format mp3 "URL"`|Скачать только аудио в mp3|
|`yt-dlp -f bv+ba --merge-output-format mp4 "URL"`|Видео+звук отдельными потоками в mp4|

---

## Устранение неполадок

### Обновить при ошибке «Unsupported URL»

```bash
sudo apt upgrade yt-dlp
pip install --user -U yt-dlp
```

---

## Ссылки

- [Репозиторий yt-dlp](https://github.com/yt-dlp/yt-dlp)
