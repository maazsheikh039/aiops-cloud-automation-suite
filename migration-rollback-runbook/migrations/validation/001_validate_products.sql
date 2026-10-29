SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_name = 'products'
) AS table_exists;

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'products'
ORDER BY ordinal_position;

SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'products';
