-- 1. Monthly Revenue
SELECT 
    strftime('%Y-%m', Date) AS MonthYear,
    SUM(TotalAmount) AS TotalRevenue,
    COUNT(TransactionID) AS TotalTransactions
FROM retail_sales
GROUP BY MonthYear
ORDER BY MonthYear;

-- 2. Top 5 Products by Revenue
SELECT 
    ProductName,
    Category,
    SUM(TotalAmount) AS TotalRevenue,
    SUM(Quantity) AS TotalUnitsSold
FROM retail_sales
GROUP BY ProductName
ORDER BY TotalRevenue DESC
LIMIT 5;

-- 3. Customer Segment Performance
SELECT 
    CustomerSegment,
    COUNT(DISTINCT CustomerID) AS UniqueCustomers,
    SUM(TotalAmount) AS TotalRevenue,
    AVG(TotalAmount) AS AverageOrderValue
FROM retail_sales
GROUP BY CustomerSegment
ORDER BY TotalRevenue DESC;

-- 4. Payment Method Popularity
SELECT 
    PaymentMethod,
    COUNT(TransactionID) AS TransactionCount,
    SUM(TotalAmount) AS TotalRevenue
FROM retail_sales
GROUP BY PaymentMethod
ORDER BY TransactionCount DESC;
