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

create table `monitor_memory_host_relation` (
    `host_id` int comment '主机ID',
    `monitor_memory_id` int comment '内存监控信息ID'
) comment = '主机与主机内存监控关系表';

create table `monitor_cpu_host_relation` (
    `host_id` int comment '主机ID',
    `monitor_cpu_id` int comment 'CPU监控信息ID'
) comment = '主机与主机CPU监控关系表';
