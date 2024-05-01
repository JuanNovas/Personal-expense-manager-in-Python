-- THIS FILE IS NOT LOAD INTO THE APP, JUST FOR CHECKING THE DATABASE SCHEMA

-- All the transactions and their data

CREATE TABLE "transactions" (
    "id" INTEGER PRIMARY KEY,
    "title" TEXT NOT NULL,
    "type" TEXT CHECK("type" IN ('clothing and accessories','education','entertainment','foods','gifts and donations','health and hygiene','housing',
    'insurance','investments','others','personal care','pets','taxes and fees','technology','transportation','travel')),
    "amount" INTEGER NOT NULL,
    "date" DATE NOT NULL
);

-- Money related information that has to be preserve 

CREATE TABLE "user_data" (
    "balance" INTEGER,
    "budget" INTEGER,
    "period" INTEGER -- 1 = daily, 2 = weekly, 3 = monthly
);

-- Reminders information, same information than the transactions table, the difference
-- is that this "date" column refers to the date that the reminders nedds to be reminded.
-- And because of being in different tables help to decrase query times

CREATE TABLE "reminder" (
    "id" INTEGER PRIMARY KEY,
    "name" TEXT NOT NULL,
    "type" TEXT CHECK("type" IN ('clothing and accessories','education','entertainment','foods','gifts and donations','health and hygiene','housing',
    'insurance','investments','others','personal care','pets','taxes and fees','technology','transportation','travel')),
    "amount" INTEGER,
    "date" TEXT NOT NULL
);

-- Default data

INSERT INTO "user_data" ("balance","budget","period") VALUES (0,0,3);