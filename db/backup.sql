PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE City(
   cityId INTEGER PRIMARY KEY,
   cityName VARCHAR(80) NOT NULL
);
CREATE TABLE Connection(
   UserId INTEGER NOT NULL ,
   Token VARCHAR(255) PRIMARY KEY,
   Starting_time DATETIME NOT NULL,
   Ending_time DATETIME NOT NULL
);
INSERT INTO Connection VALUES('(1,)','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbMV0sInVzZXJuYW1lIjoic2FsdXRAZ21haWwuY29tIiwiZXhwIjoxNzEwNTIyODc4fQ.M1bxbjqP3j8cDFRNUr9fcQchy1BhJEowVTxs0Qt9SFs','2024-03-15 14:14:38.298490','2024-03-15 17:14:38.298490');
INSERT INTO Connection VALUES('(1,)','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbMV0sInVzZXJuYW1lIjoic2FsdXRAZ21haWwuY29tIiwiZXhwIjoxNzEwNTIyOTIxfQ.lVe0kh4fq9t6ywmBS1tuyJzbN0pE2a0WiimGOjM0mkc','2024-03-15 14:15:21.505173','2024-03-15 17:15:21.505173');
INSERT INTO Connection VALUES('(1,)','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbMV0sInVzZXJuYW1lIjoic2FsdXRAZ21haWwuY29tIiwiZXhwIjoxNzEwNTIyOTQzfQ.ykzqzWtU8HzR93riCSfilT9OzfCL9pqFrj88IuwMsFw','2024-03-15 14:15:43.772133','2024-03-15 17:15:43.772133');
INSERT INTO Connection VALUES('(1,)','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbMV0sInVzZXJuYW1lIjoic2FsdXRAZ21haWwuY29tIiwiZXhwIjoxNzEwNjEwODIzfQ.9TlwV8ncyaCH8Kn1hdXZwO61o-LqLmggmGf8HnCuoz0','2024-03-16 14:40:23.403395','2024-03-16 17:40:23.403395');
INSERT INTO Connection VALUES('(1,)','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbMV0sInVzZXJuYW1lIjoic2FsdXRAZ21haWwuY29tIiwiZXhwIjoxNzEwNjEyMDA2fQ.3N1sZrEsvv4hcCNxRoBJQsrmcBUxVm0xNJ3uxUkyNhA','2024-03-16 15:00:06.690881','2024-03-16 18:00:06.690881');
INSERT INTO Connection VALUES('(1,)','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbMV0sInVzZXJuYW1lIjoic2FsdXRAZ21haWwuY29tIiwiZXhwIjoxNzEwNjEyNzk5fQ.ygXeWKdsp5oFupC-v3_MiFY7sRG29LigRB473ruMyUE','2024-03-16 15:13:19.704277','2024-03-16 18:13:19.704277');
INSERT INTO Connection VALUES('(1,)','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbMV0sInVzZXJuYW1lIjoic2FsdXRAZ21haWwuY29tIiwiZXhwIjoxNzEwNjEzMzQ0fQ.d9DDQkBTMQrrODwQvwgZYzqJBgNA6DlXMJrAyoV_6AE','2024-03-16 15:22:24.573163','2024-03-16 18:22:24.573163');
CREATE TABLE UserData(
   UserId INTEGER PRIMARY KEY,
   lastName VARCHAR(80) NOT NULL,
   age INTEGER,
   email VARCHAR(255) NOT NULL,
   phone VARCHAR(255) NOT NULL,
   status VARCHAR(255) NOT NULL,
   userAddress VARCHAR(255) NOT NULL,
   password VARCHAR(255) NOT NULL,
   firstName VARCHAR(80) NOT NULL,
   cityId INTEGER NOT NULL,
   FOREIGN KEY(cityId) REFERENCES City(cityId)
);
INSERT INTO UserData VALUES(1,'salut',21,'salut@gmail.com','0102030201','2','fazfzaffaz','ab4f63f9ac65152575886860dde480a1','salut',3);
INSERT INTO UserData VALUES(2,'Doe',30,'existing@example.com','1234567890','1','123 Street','482c811da5d5b4bc6d497ffa98491e38','John',1);
CREATE TABLE Plant(
   plantID INTEGER PRIMARY KEY,
   plantDescription VARCHAR(255) NOT NULL,
   plantAdress VARCHAR(255) NOT NULL,
   name VARCHAR(80) NOT NULL,
   date DATETIME NOT NULL,
   UserId NOT NULL,
   FOREIGN KEY(UserId) REFERENCES Guardian(UserId)
);
CREATE TABLE messageHistory(
   messageId INTEGER PRIMARY KEY,
   messageDate VARCHAR(255) NOT NULL,
   content VARCHAR(255) NOT NULL,
   UserId INTEGER NOT NULL,
   FOREIGN KEY(UserId) REFERENCES Guardian(UserId)
);
CREATE TABLE PlantImages(
   ImageId INTEGER PRIMARY KEY,
   Image VARCHAR(255) NOT NULL,
   ImageDate DATETIME NOT NULL,
   UserId INT NOT NULL,
   plantID INT NOT NULL,
   FOREIGN KEY(UserId) REFERENCES Guardian(UserId),
   FOREIGN KEY(plantID) REFERENCES Plant(plantID)
);
CREATE TABLE Tip(
   tipId INTEGER PRIMARY KEY,
   tipDescription VARCHAR(255) NOT NULL,
   UserId INT NOT NULL,
   FOREIGN KEY(UserId) REFERENCES Botanist(UserId)
);
CREATE TABLE Concern(
   plantID INT NOT NULL,
   tipId INT PRIMARY KEY,
   FOREIGN KEY(plantID) REFERENCES Plant(plantID),
   FOREIGN KEY(tipId) REFERENCES Tip(tipId)
);
COMMIT;
