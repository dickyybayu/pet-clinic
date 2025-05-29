CREATE OR REPLACE FUNCTION cek_stok_vaksin()
RETURNS TRIGGER AS $$ 
DECLARE 
v_nama_vaksin varchar(100);
v_stok_sekarang  int;
BEGIN 
	select nama, stok 
	from vaksin into v_nama_vaksin, v_stok_sekarang
	where kode = new.kode_vaksin;

	IF v_stok_sekarang < 1 THEN
		RAISE EXCEPTION 'ERROR: Stok vaksin "%" tidak mencukupi untuk vaksinasi.', v_nama_vaksin;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_cek_stok_vaksin_update
BEFORE UPDATE ON KUNJUNGAN
FOR EACH ROW
WHEN (NEW.kode_vaksin IS NOT NULL AND NEW.kode_vaksin IS DISTINCT FROM OLD.kode_vaksin)
EXECUTE FUNCTION cek_stok_vaksin();	
	

CREATE OR REPLACE FUNCTION kelola_vaksin()
RETURNS TRIGGER AS $$
BEGIN
        IF OLD.kode_vaksin IS NOT NULL THEN
            UPDATE vaksin SET stok = stok + 1 WHERE kode = OLD.kode_vaksin;
        END IF;

        IF NEW.kode_vaksin IS NOT NULL THEN
            UPDATE vaksin SET stok = stok - 1 WHERE kode = NEW.kode_vaksin;
        END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_after_update_vaksin
AFTER UPDATE ON KUNJUNGAN
FOR EACH ROW
WHEN (NEW.Kode_vaksin IS DISTINCT FROM OLD.Kode_vaksin)
EXECUTE FUNCTION kelola_vaksin();


CREATE OR REPLACE FUNCTION cek_vaksin_in_kunjungan()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT kode_vaksin FROM kunjungan WHERE kode_vaksin = OLD.kode) THEN
        RAISE EXCEPTION 'ERROR: Vaksin tidak dapat dihapus dikarenakan telah digunakan untuk vaksinasi.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_cek_vaksin_in_kunjungan_before_delete
BEFORE DELETE ON VAKSIN
FOR EACH ROW
EXECUTE FUNCTION cek_vaksin_in_kunjungan();