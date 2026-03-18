<<<<<<< HEAD
-- Database initialization script for PostgreSQL
-- E-commerce Sales Data Schema

-- Drop existing tables if they exist
DROP TABLE IF EXISTS sales CASCADE;

-- Create sales table based on Amazon e-commerce dataset
CREATE TABLE IF NOT EXISTS sales (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    product_id INTEGER NOT NULL,
    product_category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    discount_percent INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    customer_region VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    rating DECIMAL(3, 1) NOT NULL,
    review_count INTEGER NOT NULL,
    discounted_price DECIMAL(10, 2) NOT NULL,
    total_revenue DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_sales_date ON sales(order_date);
CREATE INDEX idx_sales_product_category ON sales(product_category);
CREATE INDEX idx_sales_customer_region ON sales(customer_region);
CREATE INDEX idx_sales_payment_method ON sales(payment_method);
CREATE INDEX idx_sales_product_id ON sales(product_id);

-- Insert sample data from Amazon e-commerce dataset
INSERT INTO sales (order_date, product_id, product_category, price, discount_percent, quantity_sold, customer_region, payment_method, rating, review_count, discounted_price, total_revenue) VALUES
('2023-01-15', 2637, 'Books', 128.75, 10, 4, 'North America', 'Credit Card', 4.2, 156, 115.88, 463.52),
('2023-01-16', 1428, 'Fashion', 302.6, 15, 2, 'Europe', 'UPI', 3.8, 89, 257.21, 514.42),
('2023-01-17', 2518, 'Electronics', 599.99, 20, 1, 'Asia', 'Debit Card', 4.5, 312, 479.99, 479.99),
('2023-01-18', 3041, 'Books', 45.5, 5, 8, 'North America', 'Credit Card', 3.9, 203, 43.23, 345.84),
('2023-01-19', 2156, 'Home & Kitchen', 189.99, 25, 3, 'South America', 'UPI', 4.1, 178, 142.49, 427.47),
('2023-01-20', 1834, 'Electronics', 899.5, 30, 1, 'Asia', 'Credit Card', 4.6, 421, 629.65, 629.65),
('2023-01-21', 2745, 'Fashion', 75.0, 10, 5, 'Europe', 'Debit Card', 3.7, 134, 67.5, 337.5),
('2023-01-22', 1567, 'Books', 32.99, 0, 6, 'North America', 'Credit Card', 4.3, 89, 32.99, 197.94),
('2023-01-23', 3214, 'Home & Kitchen', 250.0, 20, 2, 'Asia', 'UPI', 4.0, 267, 200.0, 400.0),
('2023-01-24', 2901, 'Sports', 120.0, 15, 4, 'South America', 'Debit Card', 3.6, 145, 102.0, 408.0),
('2023-01-25', 1923, 'Electronics', 1299.99, 35, 1, 'Europe', 'Credit Card', 4.7, 534, 844.99, 844.99),
('2023-01-26', 2456, 'Fashion', 89.99, 12, 3, 'North America', 'UPI', 3.9, 92, 79.19, 237.57),
('2023-01-27', 3005, 'Books', 52.0, 8, 7, 'Asia', 'Credit Card', 4.1, 156, 47.84, 334.88),
('2023-01-28', 1645, 'Home & Kitchen', 175.0, 18, 4, 'Europe', 'Debit Card', 4.2, 289, 143.5, 574.0),
('2023-01-29', 2534, 'Electronics', 450.0, 22, 2, 'North America', 'Credit Card', 4.4, 378, 351.0, 702.0),
('2023-02-01', 1789, 'Sports', 98.5, 10, 5, 'South America', 'UPI', 3.8, 167, 88.65, 443.25),
('2023-02-02', 2876, 'Fashion', 145.0, 20, 3, 'Asia', 'Credit Card', 4.0, 201, 116.0, 348.0),
('2023-02-03', 1234, 'Books', 68.5, 6, 4, 'Europe', 'Debit Card', 4.3, 224, 64.39, 257.56),
('2023-02-04', 3102, 'Home & Kitchen', 299.99, 25, 2, 'North America', 'Credit Card', 4.5, 456, 224.99, 449.98),
('2023-02-05', 2567, 'Electronics', 799.0, 28, 1, 'Asia', 'UPI', 4.6, 512, 575.28, 575.28),
('2023-02-06', 1956, 'Sports', 145.0, 15, 6, 'South America', 'Debit Card', 3.9, 178, 123.25, 739.5),
('2023-02-07', 2734, 'Fashion', 55.0, 10, 8, 'Europe', 'Credit Card', 3.7, 145, 49.5, 396.0),
('2023-02-08', 1498, 'Books', 95.0, 12, 3, 'North America', 'UPI', 4.2, 267, 83.6, 250.8),
('2023-02-09', 2945, 'Home & Kitchen', 199.99, 20, 4, 'Asia', 'Credit Card', 4.1, 334, 159.99, 639.96),
('2023-02-10', 3187, 'Electronics', 329.99, 15, 2, 'Europe', 'Debit Card', 4.4, 389, 280.49, 560.98),
('2023-02-11', 1823, 'Fashion', 125.0, 18, 5, 'North America', 'Credit Card', 3.8, 156, 102.5, 512.5),
('2023-02-12', 2601, 'Sports', 212.5, 22, 3, 'South America', 'UPI', 4.0, 234, 165.75, 497.25),
('2023-02-13', 1645, 'Books', 78.0, 7, 6, 'Asia', 'Debit Card', 4.3, 289, 72.54, 435.24),
('2023-02-14', 2856, 'Home & Kitchen', 420.0, 30, 1, 'Europe', 'Credit Card', 4.6, 445, 294.0, 294.0),
('2023-02-15', 3045, 'Electronics', 1099.99, 35, 1, 'North America', 'UPI', 4.7, 678, 714.99, 714.99),
('2023-02-16', 2134, 'Fashion', 165.0, 12, 4, 'Asia', 'Credit Card', 3.9, 123, 145.2, 580.8),
('2023-02-17', 1789, 'Sports', 89.99, 10, 7, 'South America', 'Debit Card', 3.8, 198, 80.99, 566.93),
('2023-02-18', 2945, 'Books', 112.0, 15, 3, 'Europe', 'Credit Card', 4.1, 267, 95.2, 285.6),
('2023-02-19', 1523, 'Home & Kitchen', 280.0, 25, 2, 'North America', 'UPI', 4.4, 356, 210.0, 420.0),
('2023-02-20', 2678, 'Electronics', 549.99, 20, 2, 'Asia', 'Debit Card', 4.5, 489, 439.99, 879.98),
('2023-03-01', 1834, 'Fashion', 95.0, 8, 6, 'Europe', 'Credit Card', 4.0, 145, 87.4, 524.4),
('2023-03-02', 2456, 'Sports', 178.5, 16, 4, 'North America', 'UPI', 3.9, 267, 150.14, 600.56),
('2023-03-03', 1645, 'Books', 145.0, 10, 5, 'South America', 'Credit Card', 4.2, 334, 130.5, 652.5),
('2023-03-04', 2987, 'Home & Kitchen', 350.0, 28, 1, 'Asia', 'Debit Card', 4.3, 512, 252.0, 252.0),
('2023-03-05', 3102, 'Electronics', 679.99, 22, 1, 'Europe', 'Credit Card', 4.6, 578, 529.99, 529.99),
('2023-03-06', 2234, 'Fashion', 210.0, 15, 3, 'North America', 'UPI', 3.8, 178, 178.5, 535.5),
('2023-03-07', 1901, 'Sports', 125.0, 12, 5, 'Asia', 'Debit Card', 4.1, 223, 110.0, 550.0),
('2023-03-08', 2678, 'Books', 89.99, 6, 4, 'South America', 'Credit Card', 4.4, 289, 84.59, 338.36),
('2023-03-09', 3245, 'Home & Kitchen', 299.99, 20, 3, 'Europe', 'UPI', 4.2, 401, 239.99, 719.97),
('2023-03-10', 1567, 'Electronics', 899.99, 30, 1, 'North America', 'Debit Card', 4.7, 645, 629.99, 629.99),
('2023-03-11', 2456, 'Fashion', 75.5, 10, 8, 'Asia', 'Credit Card', 3.9, 156, 67.95, 543.6),
('2023-03-12', 1834, 'Sports', 195.0, 18, 4, 'South America', 'UPI', 4.0, 278, 159.9, 639.6),
('2023-03-13', 2945, 'Books', 62.0, 5, 7, 'Europe', 'Credit Card', 4.3, 312, 58.9, 412.3),
('2023-03-14', 1723, 'Home & Kitchen', 425.0, 25, 2, 'North America', 'Debit Card', 4.5, 468, 318.75, 637.5),
('2023-03-15', 2867, 'Electronics', 749.99, 25, 1, 'Asia', 'UPI', 4.6, 567, 562.49, 562.49),
('2023-03-16', 1645, 'Fashion', 135.0, 14, 5, 'Europe', 'Credit Card', 3.8, 167, 116.1, 580.5),
('2023-03-17', 2734, 'Sports', 168.75, 11, 4, 'North America', 'Debit Card', 4.2, 234, 150.19, 600.76),
('2023-03-18', 1901, 'Books', 98.0, 9, 6, 'South America', 'UPI', 4.1, 345, 89.18, 535.08),
('2023-03-19', 3056, 'Home & Kitchen', 299.0, 22, 3, 'Asia', 'Credit Card', 4.4, 489, 233.22, 699.66),
('2023-03-20', 2567, 'Electronics', 599.99, 26, 1, 'Europe', 'Debit Card', 4.5, 523, 443.99, 443.99);

-- Grant permissions (uncomment if using a separate user)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bi_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bi_user;
=======
-- Database initialization script for PostgreSQL
-- E-commerce Sales Data Schema

-- Drop existing tables if they exist
DROP TABLE IF EXISTS sales CASCADE;

-- Create sales table based on Amazon e-commerce dataset
CREATE TABLE IF NOT EXISTS sales (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    product_id INTEGER NOT NULL,
    product_category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    discount_percent INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    customer_region VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    rating DECIMAL(3, 1) NOT NULL,
    review_count INTEGER NOT NULL,
    discounted_price DECIMAL(10, 2) NOT NULL,
    total_revenue DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_sales_date ON sales(order_date);
CREATE INDEX idx_sales_product_category ON sales(product_category);
CREATE INDEX idx_sales_customer_region ON sales(customer_region);
CREATE INDEX idx_sales_payment_method ON sales(payment_method);
CREATE INDEX idx_sales_product_id ON sales(product_id);

-- Insert sample data from Amazon e-commerce dataset
INSERT INTO sales (order_date, product_id, product_category, price, discount_percent, quantity_sold, customer_region, payment_method, rating, review_count, discounted_price, total_revenue) VALUES
('2023-01-15', 2637, 'Books', 128.75, 10, 4, 'North America', 'Credit Card', 4.2, 156, 115.88, 463.52),
('2023-01-16', 1428, 'Fashion', 302.6, 15, 2, 'Europe', 'UPI', 3.8, 89, 257.21, 514.42),
('2023-01-17', 2518, 'Electronics', 599.99, 20, 1, 'Asia', 'Debit Card', 4.5, 312, 479.99, 479.99),
('2023-01-18', 3041, 'Books', 45.5, 5, 8, 'North America', 'Credit Card', 3.9, 203, 43.23, 345.84),
('2023-01-19', 2156, 'Home & Kitchen', 189.99, 25, 3, 'South America', 'UPI', 4.1, 178, 142.49, 427.47),
('2023-01-20', 1834, 'Electronics', 899.5, 30, 1, 'Asia', 'Credit Card', 4.6, 421, 629.65, 629.65),
('2023-01-21', 2745, 'Fashion', 75.0, 10, 5, 'Europe', 'Debit Card', 3.7, 134, 67.5, 337.5),
('2023-01-22', 1567, 'Books', 32.99, 0, 6, 'North America', 'Credit Card', 4.3, 89, 32.99, 197.94),
('2023-01-23', 3214, 'Home & Kitchen', 250.0, 20, 2, 'Asia', 'UPI', 4.0, 267, 200.0, 400.0),
('2023-01-24', 2901, 'Sports', 120.0, 15, 4, 'South America', 'Debit Card', 3.6, 145, 102.0, 408.0),
('2023-01-25', 1923, 'Electronics', 1299.99, 35, 1, 'Europe', 'Credit Card', 4.7, 534, 844.99, 844.99),
('2023-01-26', 2456, 'Fashion', 89.99, 12, 3, 'North America', 'UPI', 3.9, 92, 79.19, 237.57),
('2023-01-27', 3005, 'Books', 52.0, 8, 7, 'Asia', 'Credit Card', 4.1, 156, 47.84, 334.88),
('2023-01-28', 1645, 'Home & Kitchen', 175.0, 18, 4, 'Europe', 'Debit Card', 4.2, 289, 143.5, 574.0),
('2023-01-29', 2534, 'Electronics', 450.0, 22, 2, 'North America', 'Credit Card', 4.4, 378, 351.0, 702.0),
('2023-02-01', 1789, 'Sports', 98.5, 10, 5, 'South America', 'UPI', 3.8, 167, 88.65, 443.25),
('2023-02-02', 2876, 'Fashion', 145.0, 20, 3, 'Asia', 'Credit Card', 4.0, 201, 116.0, 348.0),
('2023-02-03', 1234, 'Books', 68.5, 6, 4, 'Europe', 'Debit Card', 4.3, 224, 64.39, 257.56),
('2023-02-04', 3102, 'Home & Kitchen', 299.99, 25, 2, 'North America', 'Credit Card', 4.5, 456, 224.99, 449.98),
('2023-02-05', 2567, 'Electronics', 799.0, 28, 1, 'Asia', 'UPI', 4.6, 512, 575.28, 575.28),
('2023-02-06', 1956, 'Sports', 145.0, 15, 6, 'South America', 'Debit Card', 3.9, 178, 123.25, 739.5),
('2023-02-07', 2734, 'Fashion', 55.0, 10, 8, 'Europe', 'Credit Card', 3.7, 145, 49.5, 396.0),
('2023-02-08', 1498, 'Books', 95.0, 12, 3, 'North America', 'UPI', 4.2, 267, 83.6, 250.8),
('2023-02-09', 2945, 'Home & Kitchen', 199.99, 20, 4, 'Asia', 'Credit Card', 4.1, 334, 159.99, 639.96),
('2023-02-10', 3187, 'Electronics', 329.99, 15, 2, 'Europe', 'Debit Card', 4.4, 389, 280.49, 560.98),
('2023-02-11', 1823, 'Fashion', 125.0, 18, 5, 'North America', 'Credit Card', 3.8, 156, 102.5, 512.5),
('2023-02-12', 2601, 'Sports', 212.5, 22, 3, 'South America', 'UPI', 4.0, 234, 165.75, 497.25),
('2023-02-13', 1645, 'Books', 78.0, 7, 6, 'Asia', 'Debit Card', 4.3, 289, 72.54, 435.24),
('2023-02-14', 2856, 'Home & Kitchen', 420.0, 30, 1, 'Europe', 'Credit Card', 4.6, 445, 294.0, 294.0),
('2023-02-15', 3045, 'Electronics', 1099.99, 35, 1, 'North America', 'UPI', 4.7, 678, 714.99, 714.99),
('2023-02-16', 2134, 'Fashion', 165.0, 12, 4, 'Asia', 'Credit Card', 3.9, 123, 145.2, 580.8),
('2023-02-17', 1789, 'Sports', 89.99, 10, 7, 'South America', 'Debit Card', 3.8, 198, 80.99, 566.93),
('2023-02-18', 2945, 'Books', 112.0, 15, 3, 'Europe', 'Credit Card', 4.1, 267, 95.2, 285.6),
('2023-02-19', 1523, 'Home & Kitchen', 280.0, 25, 2, 'North America', 'UPI', 4.4, 356, 210.0, 420.0),
('2023-02-20', 2678, 'Electronics', 549.99, 20, 2, 'Asia', 'Debit Card', 4.5, 489, 439.99, 879.98),
('2023-03-01', 1834, 'Fashion', 95.0, 8, 6, 'Europe', 'Credit Card', 4.0, 145, 87.4, 524.4),
('2023-03-02', 2456, 'Sports', 178.5, 16, 4, 'North America', 'UPI', 3.9, 267, 150.14, 600.56),
('2023-03-03', 1645, 'Books', 145.0, 10, 5, 'South America', 'Credit Card', 4.2, 334, 130.5, 652.5),
('2023-03-04', 2987, 'Home & Kitchen', 350.0, 28, 1, 'Asia', 'Debit Card', 4.3, 512, 252.0, 252.0),
('2023-03-05', 3102, 'Electronics', 679.99, 22, 1, 'Europe', 'Credit Card', 4.6, 578, 529.99, 529.99),
('2023-03-06', 2234, 'Fashion', 210.0, 15, 3, 'North America', 'UPI', 3.8, 178, 178.5, 535.5),
('2023-03-07', 1901, 'Sports', 125.0, 12, 5, 'Asia', 'Debit Card', 4.1, 223, 110.0, 550.0),
('2023-03-08', 2678, 'Books', 89.99, 6, 4, 'South America', 'Credit Card', 4.4, 289, 84.59, 338.36),
('2023-03-09', 3245, 'Home & Kitchen', 299.99, 20, 3, 'Europe', 'UPI', 4.2, 401, 239.99, 719.97),
('2023-03-10', 1567, 'Electronics', 899.99, 30, 1, 'North America', 'Debit Card', 4.7, 645, 629.99, 629.99),
('2023-03-11', 2456, 'Fashion', 75.5, 10, 8, 'Asia', 'Credit Card', 3.9, 156, 67.95, 543.6),
('2023-03-12', 1834, 'Sports', 195.0, 18, 4, 'South America', 'UPI', 4.0, 278, 159.9, 639.6),
('2023-03-13', 2945, 'Books', 62.0, 5, 7, 'Europe', 'Credit Card', 4.3, 312, 58.9, 412.3),
('2023-03-14', 1723, 'Home & Kitchen', 425.0, 25, 2, 'North America', 'Debit Card', 4.5, 468, 318.75, 637.5),
('2023-03-15', 2867, 'Electronics', 749.99, 25, 1, 'Asia', 'UPI', 4.6, 567, 562.49, 562.49),
('2023-03-16', 1645, 'Fashion', 135.0, 14, 5, 'Europe', 'Credit Card', 3.8, 167, 116.1, 580.5),
('2023-03-17', 2734, 'Sports', 168.75, 11, 4, 'North America', 'Debit Card', 4.2, 234, 150.19, 600.76),
('2023-03-18', 1901, 'Books', 98.0, 9, 6, 'South America', 'UPI', 4.1, 345, 89.18, 535.08),
('2023-03-19', 3056, 'Home & Kitchen', 299.0, 22, 3, 'Asia', 'Credit Card', 4.4, 489, 233.22, 699.66),
('2023-03-20', 2567, 'Electronics', 599.99, 26, 1, 'Europe', 'Debit Card', 4.5, 523, 443.99, 443.99);

-- Grant permissions (uncomment if using a separate user)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bi_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bi_user;
>>>>>>> e517d8130e130853f1f9ba7259a224e88643b9cd
