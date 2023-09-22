DROP database if exists `chatAppDB`;

CREATE DATABASE chatAppDB;

USE chatAppDB;


CREATE TABLE `Users`(
    `Userid` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Username` BIGINT NULL,
    `Password` VARCHAR(255) NULL
);
CREATE TABLE `Rooms`(
    `RoomID` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `RoomName` VARCHAR(255) NULL
);
CREATE TABLE `Messages`(
    `MessageID` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `UserID` INT UNSIGNED NOT NULL,
    `RoomName` VARCHAR(255) NOT NULL,
    `Content` VARCHAR(255) NOT NULL,
    `Timestamp` DATETIME NULL
);
CREATE INDEX messages_roomName_foreign ON Rooms (RoomName);
ALTER TABLE
    `Messages` ADD CONSTRAINT `messages_userid_foreign` FOREIGN KEY(`UserID`) REFERENCES `Users`(`Userid`);
ALTER TABLE
    `Messages` ADD CONSTRAINT `messages_roomName_foreign` FOREIGN KEY(`RoomName`) REFERENCES `Rooms`(`RoomName`);

