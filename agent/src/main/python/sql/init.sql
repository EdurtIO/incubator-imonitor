CREATE TABLE `host` (
    `host`            varchar(255),
    `port`            varchar(255),
    `username`        varchar(255),
    `password`        varchar(255),
    `command`         varchar(255),
    `command_start`   varchar(255),
    `command_stop`    varchar(255),
    `command_restart` varchar(255)
) COMMENT ='主机表';
