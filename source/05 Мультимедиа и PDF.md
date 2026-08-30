# 05 — Мультимедиа и PDF

> Аудио/видео, торрент-клиент и работа с документами: просмотр, сжатие,
> объединение и разбиение PDF.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Медиа

```bash
sudo apt install ffmpeg vlc qbittorrent -y
```

- `ffmpeg` — конвертация, обрезка, извлечение звука из командной строки
- `vlc` — универсальный медиаплеер
- `qbittorrent` — торрент-клиент

---

## Шаг 2 — PDF и документы

```bash
sudo apt install ghostscript okular okular-extra-backends pdfarranger -y
```

- `ghostscript` (gs) — конвертация и сжатие PDF/PS из CLI
- `okular` — просмотрщик PDF, DJVU, EPUB, MOBI (KDE)
- `okular-extra-backends` — дополнительные форматы
- `pdfarranger` — графический редактор PDF: объединение, разбиение, поворот страниц

---

## Шаг 3 — Проверка

```bash
ffmpeg -version | head -n1
vlc --version | head -n1
qbittorrent --version
gs --version
pdfarranger --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`ffmpeg -i input.mkv out.mp4`|Конвертировать формат|
|`ffmpeg -i input.mp4 -vn out.mp3`|Извлечь звук|
|`ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy cut.mp4`|Вырезать фрагмент без перекодирования|
|`gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -o small.pdf big.pdf`|Сжать PDF|
|`gs -sDEVICE=pdfwrite -o out.pdf in.ps`|PS в PDF|
|`okular file.pdf`|Открыть документ|

---

## Устранение неполадок

- **ffmpeg «Conversion failed!»** — убери `-c copy`, нужен перекодинг.
- **VLC нет звука/видео** — Инструменты → Настройки → Ввод/Кодеки: отключи аппаратное декодирование.
- **qBittorrent через VPN/прокси** — Настройки → Соединение: укажи прокси или интерфейс.
