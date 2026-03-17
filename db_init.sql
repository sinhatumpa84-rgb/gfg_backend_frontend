-- Database initialization script for PostgreSQL
-- This script creates the initial tables and populates sample data

-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    date DATE,
    region VARCHAR(50),
    product_category VARCHAR(100),
    product_name VARCHAR(100),
    revenue DECIMAL(10, 2),
    quantity INTEGER,
    salesperson VARCHAR(100)
);

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    salary DECIMAL(10, 2),
    hire_date DATE
);

-- Create indexes for better performance
CREATE INDEX idx_sales_region ON sales(region);
CREATE INDEX idx_sales_date ON sales(date);
CREATE INDEX idx_sales_product_category ON sales(product_category);
CREATE INDEX idx_sales_salesperson ON sales(salesperson);

-- Insert sample sales data
INSERT INTO sales (date, region, product_category, product_name, revenue, quantity, salesperson) VALUES
('2024-01-01', 'North', 'Electronics', 'Laptop', 5000.00, 2, 'John'),
('2024-01-02', 'South', 'Furniture', 'Desk', 800.00, 1, 'Sarah'),
('2024-01-03', 'East', 'Electronics', 'Phone', 1200.00, 3, 'Mike'),
('2024-01-04', 'West', 'Clothing', 'Shirt', 50.00, 5, 'Emma'),
('2024-01-05', 'North', 'Electronics', 'Tablet', 2000.00, 1, 'John'),
('2024-02-01', 'South', 'Electronics', 'Laptop', 5000.00, 1, 'Sarah'),
('2024-02-02', 'East', 'Furniture', 'Chair', 500.00, 4, 'Mike'),
('2024-02-03', 'West', 'Electronics', 'Monitor', 600.00, 2, 'Emma'),
('2024-03-01', 'North', 'Clothing', 'Jacket', 150.00, 2, 'John'),
('2024-03-02', 'South', 'Furniture', 'Table', 1500.00, 1, 'Sarah'),
('2024-03-03', 'East', 'Electronics', 'Keyboard', 200.00, 5, 'Mike'),
('2024-03-04', 'West', 'Furniture', 'Bookshelf', 400.00, 1, 'Emma'),
('2024-01-06', 'North', 'Furniture', 'Sofa', 2500.00, 1, 'John'),
('2024-01-07', 'South', 'Clothing', 'Pants', 80.00, 6, 'Sarah'),
('2024-02-04', 'East', 'Clothing', 'Dress', 120.00, 3, 'Mike');

-- Insert sample employees data
INSERT INTO employees (name, department, salary, hire_date) VALUES
('John', 'Sales', 50000.00, '2020-01-15'),
('Sarah', 'Sales', 55000.00, '2019-06-01'),
('Mike', 'Sales', 52000.00, '2021-03-10'),
('Emma', 'Sales', 48000.00, '2022-01-20');

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bi_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bi_user;
