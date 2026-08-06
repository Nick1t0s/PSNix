# Ghostscript

> Интерпретатор PostScript и PDF. Используется для конвертации, сжатия и обработки PDF из командной строки.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install ghostscript -y
```

---

## Шаг 2 — Проверка

```bash
gs --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`gs -sDEVICE=pdfwrite -o out.pdf in.ps`|Конвертировать PS в PDF|
|`gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -o small.pdf big.pdf`|Сжать PDF|
|`gs -sDEVICE=png16m -r150 -o out.png in.pdf`|PDF в PNG|

---

## Устранение неполадок

### Ошибка прав на запись

Ghostscript требует прав на создание файла в текущей директории — запускай из папки, где есть права на запись.

---

## Ссылки

- [ghostscript.com](https://www.ghostscript.com/)
