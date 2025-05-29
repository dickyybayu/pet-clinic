CREATE OR REPLACE FUNCTION prevent_duplicate_jenis_hewan()
RETURNS trigger AS $$
DECLARE
    existing_id UUID;
BEGIN
    SELECT id INTO existing_id
    FROM JENIS_HEWAN
    WHERE LOWER(nama) = LOWER(NEW.nama);

    IF existing_id IS NOT NULL THEN
        RAISE EXCEPTION USING MESSAGE = format(
            'Jenis hewan "%s" sudah terdaftar dengan ID %s',
            NEW.nama, existing_id
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_prevent_duplicate_jenis_hewan
BEFORE INSERT ON JENIS_HEWAN
FOR EACH ROW
EXECUTE FUNCTION prevent_duplicate_jenis_hewan();



CREATE OR REPLACE FUNCTION prevent_delete_hewan()
RETURNS trigger AS $$
DECLARE
    aktif_count INT;
    nama_pemilik TEXT;
BEGIN
    SELECT COUNT(*) INTO aktif_count
    FROM KUNJUNGAN
    WHERE nama_hewan = OLD.nama
      AND no_identitas_klien = OLD.no_identitas_klien
      AND timestamp_akhir IS NULL;

    IF aktif_count > 0 THEN
        SELECT COALESCE(
            i.nama_depan || ' ' || COALESCE(i.nama_tengah || ' ', '') || i.nama_belakang,
            p.nama_perusahaan
        ) INTO nama_pemilik
        FROM KLIEN k
        LEFT JOIN INDIVIDU i ON i.no_identitas_klien = k.no_identitas
        LEFT JOIN PERUSAHAAN p ON p.no_identitas_klien = k.no_identitas
        WHERE k.no_identitas = OLD.no_identitas_klien;

        RAISE EXCEPTION USING
            MESSAGE = format(
                'Hewan "%s" milik "%s" masih memiliki kunjungan aktif sehingga tidak dapat dihapus.',
                OLD.nama, nama_pemilik
            );
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_prevent_delete_hewan
BEFORE DELETE ON HEWAN
FOR EACH ROW
EXECUTE FUNCTION prevent_delete_hewan();