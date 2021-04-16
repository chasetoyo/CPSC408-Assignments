create table FoodType(
    FoodTypeID int AUTO_INCREMENT,
    Name varchar(64),
    PRIMARY KEY (FoodTypeID)
);

create table MenuItem(
    MenuItemID INT AUTO_INCREMENT,
    Name varchar(64),
    FoodTypeID int,
    primary key (MenuItemID),
    foreign key (FoodTypeID) references FoodType(FoodTypeID)
);

create table Menu(
   MenuID INT AUTO_INCREMENT,
   MenuItemID INT,
   Price DEC(5, 2),
   PRIMARY KEY (MenuID),
   FOREIGN KEY (MenuItemID) REFERENCES MenuItem(MenuItemID)
);

create table Reservation(
    ReservationID int auto_increment,
    Email varchar(128),
    PartySize int,
    ReservationTime datetime,
    primary key (ReservationID)
);

create table Tab(
    TabID int auto_increment,
    ReservationID int,
    primary key (TabID),
    foreign key (ReservationID) references Reservation(ReservationID)
);

create table OrderItem(
    OrderItemID int auto_increment,
    OrderID int,
    MenuItemID int,
    Quantity int,
    primary key (OrderItemID),
    foreign key (OrderID) references Tab(TabID),
    foreign key (MenuItemID) references MenuItem(MenuItemID)
);