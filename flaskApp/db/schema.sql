/*
 Navicat Premium Data Transfer

 Source Server         : flask_sippas
 Source Server Type    : SQLite
 Source Server Version : 3026000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3026000
 File Encoding         : 65001

 Date: 26/03/2019 13:27:03
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for posts
-- ----------------------------
DROP TABLE IF EXISTS "posts";
CREATE TABLE "posts" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "title" text,
  "body" TEXT,
  "teaser" text,
  "tags" TEXT,
  "is_sticky" integer,
  "author_id" text,
  "created_at" TEXT,
  "updated_at" text,
  "published_at" TEXT
);

-- ----------------------------
-- Auto increment value for posts
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 1013 WHERE name = 'posts';

-- ----------------------------
-- Indexes structure for table posts
-- ----------------------------
CREATE INDEX "main"."tags_idx"
ON "posts" (
  "tags" COLLATE BINARY ASC
);

PRAGMA foreign_keys = true;
