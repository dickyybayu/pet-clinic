CREATE OR REPLACE FUNCTION cek_validasi_waktu_kunjungan()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.timestamp_akhir IS NOT NULL AND NEW.timestamp_akhir < NEW.timestamp_awal THEN
        RAISE EXCEPTION 'ERROR: Timestamp akhir kunjungan tidak boleh lebih awal dari timestamp awal.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validasi_waktu_kunjungan
BEFORE INSERT OR UPDATE ON KUNJUNGAN
FOR EACH ROW
EXECUTE FUNCTION cek_validasi_waktu_kunjungan();

REATE OR REPLACE FUNCTION cek_kepemilikan_hewan()
RETURNS TRIGGER AS $$
DECLARE
    pemilik TEXT;
BEGIN
    SELECT h.no_identitas_klien INTO pemilik
    FROM HEWAN h
    WHERE h.nama = NEW.nama_hewan AND h.no_identitas_klien = NEW.no_identitas_klien;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'ERROR: Hewan "%" tidak terdaftar atas nama pemilik "%".', NEW.nama_hewan, NEW.no_identitas_klien;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_cek_kepemilikan_hewan
BEFORE INSERT OR UPDATE ON KUNJUNGAN
FOR EACH ROW
EXECUTE FUNCTION cek_kepemilikan_hewan();