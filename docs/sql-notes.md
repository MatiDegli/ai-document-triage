# SQL Notes

These queries use the `documents` table created by the application migrations.

## Insert a document

`INSERT` adds a new row to a table. PostgreSQL generates the `id`,
`created_at`, and initial `updated_at` values using their configured defaults.
SQLAlchemy updates `updated_at` when a modified object is persisted.

```sql
INSERT INTO documents (title, content)
VALUES ('Example', 'Document content');
```

## Get a document by ID

`SELECT` reads data. This query returns the document whose `id` is `1`.

```sql
SELECT id, title, content, created_at, updated_at
FROM documents
WHERE id = 1;
```

## List all documents

This query returns every document, newest first.

```sql
SELECT id, title, content, created_at, updated_at
FROM documents
ORDER BY created_at DESC;
```

## Count documents

`COUNT(*)` returns the number of rows in the table.

```sql
SELECT COUNT(*) AS document_count
FROM documents;
```
