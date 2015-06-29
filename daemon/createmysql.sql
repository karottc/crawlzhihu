
CREATE DATABASE IF NOT EXISTS zhihu DEFAULT CHARSET utf8;

USE zhihu;

#创建知乎每日吐槽索引的表
CREATE TABLE t_zhihu_daily_index
(
    fid bigint(20) unsigned PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fupdatetime bigint(20) unsigned NOT NULL DEFAULT '0',
    fstoryid bigint(20) unsigned NOT NULL DEFAULT '0',
    ftitlename varchar(64),
    fnum bigint(20) unsigned,
    frecomm longtext,
    ftitlepic varchar(64),
    ftitlebigpic varchar(64),
    fdisplaydate varchar(64),
    fext1 bigint(20) unsigned,
    fext2 bigint(20) unsigned,
    fext3 varchar(256),
    fext4 varchar(256),
    INDEX(fstoryid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#创建知乎每日吐槽存取内容的表
CREATE TABLE t_zhihu_daily_story
(
    fid bigint(20) unsigned PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fstoryid bigint(20) unsigned NOT NULL DEFAULT '0',
    ftitle text,
    fnum bigint(20) unsigned,
    fanwser longtext,
    fviewmore varchar(64),
    fext1 bigint(20) unsigned,
    fext2 bigint(20) unsigned,
    fext3 varchar(256),
    fext4 varchar(256),
    INDEX(fstoryid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;