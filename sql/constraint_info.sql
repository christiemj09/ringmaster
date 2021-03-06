-- Get info on the constraints in the database.

CREATE VIEW constraint_info AS
    SELECT pn.nspname AS schema_name,
           pc.relname AS rel_name,
           pco.conname AS constraint_name,
           pg_get_constraintdef(pco.oid, TRUE) AS constraint_def
    FROM pg_namespace pn,
         pg_constraint pco,
         pg_class pc
    WHERE pn.oid = pco.connamespace
      AND pc.oid = pco.conrelid;
