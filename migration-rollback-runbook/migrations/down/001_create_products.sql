BEGIN;
DROP TRIGGER IF EXISTS trg_update_products_modtime ON products;
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP TABLE IF EXISTS products CASCADE;
COMMIT;

