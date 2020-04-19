create table `monitor_memory_host_relation` (
    `host_id` int comment '主机ID',
    `monitor_memory_id` int comment '内存监控信息ID'
) comment = '主机与主机内存监控关系表';

create table `monitor_cpu_host_relation` (
    `host_id` int comment '主机ID',
    `monitor_cpu_id` int comment 'CPU监控信息ID'
) comment = '主机与主机CPU监控关系表';

alter table user add column website varchar(100) after password;
alter table user add column description text after password;
alter table user add column position varchar(100) after password;

create table `user_logging_login_relation` (
    `user_id` int comment '用户ID',
    `logging_login_id` int comment '登录日志ID'
) comment = '用户与登录日志关系表';

alter table user add column avatar varchar(200) after website;

create table `user_host_command_execute_relation` (
    `user_id` int comment '用户ID',
    `host_id` int comment '主机ID',
    `command_execute_id` int comment '命令历史ID'
) comment = '用户主机执行命令关系表';


create table `user_host_connection` (
    `user_id` int comment '用户ID',
    `host_id` int comment '主机ID',
    `connection_id` int comment '连接ID'
) comment = '用户主机连接关系表';