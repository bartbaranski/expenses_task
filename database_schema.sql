CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE expense_type (
    expense_type_id SERIAL PRIMARY KEY,
    name             VARCHAR(100) NOT NULL
);


CREATE TABLE date_dim (
    date_id     SERIAL PRIMARY KEY,
    year        INTEGER NOT NULL,
    month       VARCHAR(10) NOT NULL,
    quarter     INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4)
);

CREATE TABLE expense_fact (
    expense_id      SERIAL PRIMARY KEY,
    department_id   INTEGER NOT NULL
        REFERENCES department(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    expense_type_id INTEGER NOT NULL
        REFERENCES expense_type(expense_type_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    date_id         INTEGER NOT NULL
        REFERENCES date_dim(date_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    amount          NUMERIC(15,2) NOT NULL
);

CREATE INDEX idx_expense_fact_department    ON expense_fact(department_id);
CREATE INDEX idx_expense_fact_date          ON expense_fact(date_id);
CREATE INDEX idx_expense_fact_dept_date     ON expense_fact(department_id, date_id);
