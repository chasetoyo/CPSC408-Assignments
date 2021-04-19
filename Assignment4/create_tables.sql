create table if not exists FoodType(
    FoodTypeID int AUTO_INCREMENT,
    Name varchar(64),
    PRIMARY KEY (FoodTypeID)
);

create table if not exists MenuItem(
    MenuItemID INT AUTO_INCREMENT,
    Name varchar(64),
    FoodTypeID int,
    primary key (MenuItemID),
    foreign key (FoodTypeID) references FoodType(FoodTypeID)
);

create table if not exists Menu(
   MenuID INT AUTO_INCREMENT,
   MenuItemID INT,
   Price DEC(5, 2),
   PRIMARY KEY (MenuID),
   FOREIGN KEY (MenuItemID) REFERENCES MenuItem(MenuItemID)
);

create table if not exists Reservation(
    ReservationID int auto_increment,
    Email varchar(128),
    PartySize int,
    ReservationTime datetime,
    primary key (ReservationID)
);

create table if not exists Tab(
    TabID int auto_increment,
    ReservationID int,
    primary key (TabID),
    foreign key (ReservationID) references Reservation(ReservationID)
);

create table if not exists OrderItem(
    OrderItemID int auto_increment,
    TabID int,
    MenuItemID int,
    Quantity int,
    primary key (OrderItemID),
    foreign key (TabID) references Tab(TabID),
    foreign key (MenuItemID) references MenuItem(MenuItemID)
);