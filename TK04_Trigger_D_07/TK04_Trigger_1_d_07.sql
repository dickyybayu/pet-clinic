CREATE OR REPLACE FUNCTION hapus_jadwal_dokter_saat_nonaktif()
RETURNS TRIGGER AS $$
DECLARE
    v_email TEXT;
BEGIN
    IF NEW.tanggal_akhir_kerja IS NOT NULL AND OLD.tanggal_akhir_kerja IS DISTINCT FROM NEW.tanggal_akhir_kerja THEN
        IF EXISTS (
            SELECT 1 FROM DOKTER_HEWAN WHERE no_dokter_hewan = NEW.no_pegawai
        ) THEN
            DELETE FROM JADWAL_PRAKTIK
            WHERE no_dokter_hewan = NEW.no_pegawai;

            SELECT u.email INTO v_email
            FROM "USER" u
            JOIN PEGAWAI p ON p.email_user = u.email
            WHERE p.no_pegawai = NEW.no_pegawai;

            RAISE NOTICE 'INFO: Semua jadwal praktik dokter dengan email "%" telah dihapus karena dokter sudah tidak aktif.', v_email;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_hapus_jadwal_dokter
AFTER UPDATE ON PEGAWAI
FOR EACH ROW
EXECUTE FUNCTION hapus_jadwal_dokter_saat_nonaktif();

CREATE OR REPLACE FUNCTION check_unique_email()
RETURNS TRIGGER AS $$
DECLARE
    email_lc TEXT;
BEGIN
    email_lc := LOWER(NEW.email);

    IF EXISTS (
        SELECT 1 FROM "USER"
        WHERE LOWER(email) = email_lc
    ) THEN
        RAISE EXCEPTION 'ERROR: Email "% sudah terdaftar, gunakan email lain.', NEW.email;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_unique_email
BEFORE INSERT ON "USER"
FOR EACH ROW
EXECUTE FUNCTION check_unique_email();