# AI Image Generator API

API ini menggunakan FastAPI untuk menghasilkan gambar AI menggunakan layanan MagicStudio.

## Fitur

- Menghasilkan gambar berdasarkan prompt teks
- Menggunakan browser otomatis dengan Selenium
- Menyimpan gambar hasil generate secara lokal
- Mengembalikan gambar dalam format base64
- Menggunakan user agent acak untuk keamanan

## Persyaratan Sistem

- Python 3.8+
- Chrome/Chromium browser
- Sistem operasi yang didukung: Windows/Linux/MacOS

## Instalasi

1. Clone repositori ini
2. Install dependensi yang diperlukan:

```bash
pip install -r requirements.txt
```

## Cara Penggunaan

1. Jalankan server FastAPI:

```bash
uvicorn main_api:app --reload
```

2. Akses API melalui endpoint:

- POST `/generate`
  - Body: JSON dengan format `{"prompt": "deskripsi gambar yang diinginkan"}`
  - Contoh:
    ```json
    {
      "prompt": "beautiful sunset on the beach"
    }
    ```

3. Response yang akan diterima:

```json
{
  "status": "success",
  "image_base64": "base64_string",
  "mime_type": "image/jpeg",
  "filename": "generated_[uuid].jpg"
}
```

## Catatan Penting

- API ini menggunakan mode headless Chrome
- Setiap request akan membuat profil Chrome baru
- Timeout untuk generate gambar adalah 120 detik

## Error Handling

API akan mengembalikan response error dalam format:

```json
{
  "status": "failed",
  "message": "Pesan error"
}
```

## Keamanan

- Menggunakan user agent acak untuk setiap request
- Membersihkan profil Chrome setelah digunakan
- Menggunakan UUID untuk nama file
