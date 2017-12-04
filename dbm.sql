SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS dbmfinal;
USE dbmfinal;
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(30),
    Street VARCHAR(30),
    City VARCHAR(30),
    State VARCHAR(2),
    ZIP VARCHAR(5),
    Email VARCHAR(30) UNIQUE,
    Pwd VARCHAR(30),
    IsBusiness Boolean
) ENGINE = INNODB;

CREATE TABLE Business(
	CustomerID INT PRIMARY KEY,
    CategoryID INT,
    GrossIncome INT,
    CONSTRAINT FK_Business_CustomerID 
    	FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    	ON DELETE CASCADE,
    CONSTRAINT FK_CategoryID
    	FOREIGN KEY (CategoryID) REFERENCES BusinessCategory(CategoryID)
    	ON DELETE RESTRICT
) ENGINE = INNODB;

CREATE TABLE BusinessCategory(
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(30)
) ENGINE = INNODB;

CREATE TABLE Home(
    CustomerID INT PRIMARY KEY,
    Income INT,
    Age INT,
    Gender Boolean,
    Marriage Boolean,
    CONSTRAINT FK_Home_CustomerID 
    	FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    	ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE Products(
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(30),
    Inventory INT,
    Price DOUBLE,
    TypeID INT,
    CONSTRAINT FK_TypeID
    	FOREIGN KEY (TypeID) REFERENCES ProductType(TypeID)
    	ON DELETE RESTRICT
) ENGINE = INNODB;

CREATE TABLE ProductType(
    TypeID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(30)
) ENGINE = INNODB;

CREATE TABLE Transactions(
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    TransactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    SalespersonID INT,
    ProductID INT,
    Quantity INT,
    CustomerID INT,
    CONSTRAINT FK_SalespersonID
    	FOREIGN KEY (SalespersonID) REFERENCES Salespersons(SalespersonID)
    	ON DELETE RESTRICT,
    CONSTRAINT FK_ProductID
    	FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    	ON DELETE RESTRICT,
    CONSTRAINT FK_Transactions_CustomerID
    	FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    	ON DELETE RESTRICT
) ENGINE = INNODB;

CREATE TABLE Salespersons(
    SalespersonID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(30),
    Street VARCHAR(30),
    City VARCHAR(30),
    State VARCHAR(2),
    ZIP VARCHAR(5),
    Email VARCHAR(30) UNIQUE,
    Pwd VARCHAR(30),
    Title VARCHAR(30),
    StoreID INT,
    Salary DOUBLE,
    CONSTRAINT FK_StoreID
    	FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
    	ON DELETE RESTRICT
	ON UPDATE NO ACTION
) ENGINE = INNODB;

CREATE TABLE Stores(
    StoreID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(30),
    Street VARCHAR(30),
    City VARCHAR(30),
    State VARCHAR(2),
    ZIP VARCHAR(5),
    ManagerID INT,
    RegionID INT,
    CONSTRAINT FK_ManagerID
    	FOREIGN KEY (ManagerID) REFERENCES Salespersons(SalespersonID)
    	ON DELETE RESTRICT
	ON UPDATE NO ACTION,
    CONSTRAINT FK_RegionID
    	FOREIGN KEY (RegionID) REFERENCES Regions(RegionID)
    	ON DELETE RESTRICT
	ON UPDATE NO ACTION
) ENGINE = INNODB;

CREATE TABLE Regions(
    RegionID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(30),
    ManagerID INT,
    CONSTRAINT FK_RegionManagerID
    	FOREIGN KEY (ManagerID) REFERENCES Salespersons(SalespersonID)
    	ON DELETE RESTRICT
	ON UPDATE NO ACTION
) ENGINE = INNODB;

SET FOREIGN_KEY_CHECKS = 1;